import typing
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any, ClassVar, Generic

from pydantic import BaseModel

from ..context import TContext
from ..deferred import Deferred
from ..exceptions import DefinitionError
from ..filter import BaseFilter, Guarantee
from ..utils.narrowing import is_bot_api_type, required_fields, root_type


def _header_payload_type(cls: type) -> type[BaseModel] | None:
    """Тип из заголовка: MessageHandler[AppContext[TextMessage]] -> TextMessage."""
    for base in getattr(cls, "__orig_bases__", ()):
        origin = typing.get_origin(base)
        if not (isinstance(origin, type) and issubclass(origin, BaseHandler)):
            continue

        for ctx_type in typing.get_args(base):
            ctx_args = typing.get_args(ctx_type)
            if ctx_args and is_bot_api_type(ctx_args[0]):
                return ctx_args[0]

    return None


class BaseHandler(ABC, Generic[TContext]):
    """
    Вид обработчика (MessageHandler, CallbackQueryHandler, ...) задаёт, какое
    поле Update он получает (update_field) и какого корневого типа там объект
    (payload_type). Виды генерируются: handlers/kinds.py.
    """

    ctx: TContext
    update_field: ClassVar[str]
    payload_type: ClassVar[type[BaseModel]]
    query: ClassVar[BaseFilter[Any] | None] = None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        promised_type = _header_payload_type(cls)
        if promised_type is None:
            return

        promised_root = root_type(promised_type)
        payload_type = getattr(cls, "payload_type", None)
        if payload_type is not None and promised_root is not payload_type:
            raise DefinitionError(
                f"{cls.__name__}: в заголовке {promised_type.__name__} "
                f"({promised_root.__name__}), а этот вид обработчика получает "
                f"{payload_type.__name__} (поле {cls.update_field})"
            )

        guaranteed = cls.query.guarantee() if cls.query is not None else Guarantee()
        if guaranteed.root is not None and guaranteed.root is not promised_root:
            raise DefinitionError(
                f"{cls.__name__}: query {cls.query!r} работает с "
                f"{guaranteed.root.__name__}, а в заголовке {promised_root.__name__}"
            )

        missing = required_fields(promised_type) - guaranteed.fields
        if missing:
            raise DefinitionError(
                f"{cls.__name__}: в заголовке обещан {promised_type.__name__}, "
                f"но query {cls.query!r} не гарантирует поля: "
                f"{', '.join(sorted(missing))}"
            )

    def __init__(self, ctx: TContext) -> None:
        self.ctx = ctx

    @abstractmethod
    async def handle(self) -> Any: ...

    async def pre_handle(
        self,
    ) -> Any: ...

    async def on_error(self, exc: Exception) -> None:
        """
        Ошибка из pre_handle или handle этого хендлера (а также из мидлварей вокруг
        него). Вернулся нормально — ошибка обработана. По умолчанию не обрабатывает
        и отдаёт выше (в on_error диспетчера): `raise exc`.

        Мидлвари к этому времени уже закрылись (post_handle отработал и увидел exc),
        поэтому ctx.db и подобное здесь недоступны; ответить пользователю
        (ctx.reply_message) можно.
        """
        raise exc

    async def after_handle(self) -> None:
        """
        Вторая половина работы, уже после закрытия хендлера: handle закончился,
        мидлвари отработали (сессия БД закоммичена и закрыта), слот диспетчера свободен.
        Сюда выносят долгое ожидание (результат фоновой задачи) и отложенные действия.
        Не запускается, если хендлер или мидлварь упали. Ошибка отсюда идёт в
        on_error. Сессии БД здесь нет: нужна своя. По умолчанию ничего не делает.
        """

    def defer(
        self,
        fn: Callable[..., Awaitable[Any]],
        *args: Any,
        delay: float = 0.0,
        **kwargs: Any,
    ) -> Deferred:
        """
        Вызвать async-функцию позже, после закрытия хендлера, через delay секунд:

            sent = await self.ctx.message.reply("Код: 1234")
            self.defer(sent.delete, delay=60)

        Не запускается, если хендлер упал. Возвращает ручку с .cancel(). Таймеры живут
        в памяти: при перезапуске бота пропадают.
        """
        return self.ctx.defer(fn, *args, delay=delay, owner=self, **kwargs)

    async def filter(self) -> bool:
        if self.query is None:
            return True

        if not await self.query.check(self.ctx):
            return False

        self.ctx = self.query.narrow(self.ctx)
        return True

    def check_type_ctx(self) -> bool:
        return getattr(self.ctx.update, self.update_field) is not None
