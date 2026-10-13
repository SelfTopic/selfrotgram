from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, ClassVar, Literal

from .callback_data import CallbackPayload
from .context import BaseContext
from .exceptions import DefinitionError
from .filter.base import BaseFilter
from .keyboard import InlineKeyboard, button
from .types import DataCallbackQuery, InlineKeyboardButton, InputRichMessage


def _overridden(cls: type, base: type, name: str) -> bool:
    """
    cls.метод переопределён где-то между cls и base? classmethod через getattr всегда
    отдаёт новый bound-объект (is между двумя обращениями никогда не совпадёт, даже для
    одного и того же метода) — сравниваем __func__, саму функцию под оберткой.
    """
    return getattr(cls, name).__func__ is not getattr(base, name).__func__


@dataclass
class ViewContent:
    """Что показать: текст или Rich-сообщение, плюс свои ряды кнопок (до навигационного
    ряда, если он есть — см. Pagination)."""

    body: str | InputRichMessage
    rows: list[list[InlineKeyboardButton]] = field(default_factory=list)


class View(ABC):
    """
    Самообновляющееся сообщение: вы говорите, как оно выглядит сейчас (render) и что
    делать при нажатии (apply), View сама отправляет, правит и отвечает на callback.
    Хендлер не видит ни edit_message_text, ни callback_query.answer(), ни разбора
    данных кнопки:

        class CounterPress(CallbackPayload, prefix="counter"):
            delta: int

        class Counter(View):
            payload = CounterPress
            n = 0

            @classmethod
            async def render(cls, ctx, data):
                if data is not None:
                    cls.n += data.delta
                return ViewContent(
                    body=str(cls.n),
                    rows=[[button("+1", CounterPress(delta=1)), button("-1", CounterPress(delta=-1))]],
                )

        class Show(MessageHandler[BaseContext[TextMessage]]):
            query = Command("counter")
            async def handle(self): await Counter.show(self.ctx)

        class Pressed(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
            query = Counter.filter()
            async def handle(self): await Counter.press(self.ctx)

    payload — свой CallbackPayload (со своим prefix и полями); View не навязывает форму
    данных кнопки. apply(ctx, data) — что сделать с состоянием (обычно в БД) до
    повторного render(); по умолчанию ничего не делает — состояние может целиком жить
    в самом payload, как у счётчика выше или у Pagination ниже.

    Классы View никогда не создаются (все методы — classmethod), поэтому обычная защита
    ABC от «забыли переопределить» не работает: без инстанцирования Python её не
    проверяет. render() проверяется явно при создании класса (DefinitionError, а не
    молчаливый None в рантайме); то же в Pagination для total()/page_content().
    """

    payload: ClassVar[type[CallbackPayload]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not _overridden(cls, View, "render"):
            raise DefinitionError(f"{cls.__name__}: нужно переопределить render()")

    @classmethod
    @abstractmethod
    async def render(cls, ctx: BaseContext[Any], data: CallbackPayload | None) -> ViewContent:
        """Текущее содержимое. data — то, что только что нажали (None при первом показе)."""

    @classmethod
    async def apply(cls, ctx: BaseContext[Any], data: CallbackPayload) -> None:
        """Применить нажатие до повторного render(). По умолчанию ничего не делает."""

    @classmethod
    def _markup(cls, content: ViewContent):
        kb = InlineKeyboard()
        for row in content.rows:
            kb.row(*row)
        return kb.markup()

    @classmethod
    async def _send(cls, ctx: BaseContext[Any], content: ViewContent) -> None:
        markup = cls._markup(content)
        if isinstance(content.body, InputRichMessage):
            await ctx.reply_rich_message(content.body, reply_markup=markup)
        else:
            await ctx.reply_message(content.body, reply_markup=markup)

    @classmethod
    async def _edit(cls, ctx: BaseContext[Any], content: ViewContent) -> None:
        markup = cls._markup(content)
        if isinstance(content.body, InputRichMessage):
            await ctx.edit_message_text(rich_message=content.body, reply_markup=markup)
        else:
            await ctx.edit_message_text(text=content.body, reply_markup=markup)

    @classmethod
    async def show(cls, ctx: BaseContext[Any]) -> None:
        """Первый показ: ответить на текущее сообщение апдейта."""
        await cls._send(ctx, await cls.render(ctx, None))

    @classmethod
    async def press(cls, ctx: BaseContext[Any]) -> None:
        """Нажатие на свою кнопку: разобрать, применить, перерисовать, ответить."""
        data = cls.payload.try_unpack(ctx.callback_query.data or "")
        if data is None:
            await ctx.callback_query.answer()
            return

        await cls.apply(ctx, data)
        await cls._edit(ctx, await cls.render(ctx, data))
        await ctx.callback_query.answer()

    @classmethod
    def filter(cls) -> BaseFilter[BaseContext[DataCallbackQuery]]:
        return cls.payload.filter()


class Pagination(View):
    """
    Частный случай View: номер страницы, навигационный ряд («« N/M »»), опционально
    кнопка закрытия. Не пишите payload и render() сами — вместо них total() (сколько
    всего) и page_content() (содержимое одной уже зажатой в границы страницы):

        class Catalog(Pagination, prefix="catalog"):
            per_page = 5

            @classmethod
            async def total(cls, ctx):
                return await ctx.db.count_items()

            @classmethod
            async def page_content(cls, ctx, page):
                items = await ctx.db.items_page(page, cls.per_page)
                return ViewContent(body="\\n".join(items))

    closable = True добавляет кнопку "✕"; по умолчанию она удаляет сообщение (closed()),
    переопределите для другого поведения (например, оставить текст без клавиатуры).
    """

    per_page: ClassVar[int] = 10
    closable: ClassVar[bool] = False

    def __init_subclass__(cls, *, prefix: str, **kwargs: Any) -> None:
        class _Page(CallbackPayload, prefix=prefix):
            action: Literal["goto", "noop", "close"] = "goto"
            page: int = 0

        cls.payload = _Page
        super().__init_subclass__(**kwargs)

        for name in ("total", "page_content"):
            if not _overridden(cls, Pagination, name):
                raise DefinitionError(f"{cls.__name__}: нужно переопределить {name}()")

    @classmethod
    @abstractmethod
    async def total(cls, ctx: BaseContext[Any]) -> int:
        """Сколько всего элементов. Может ходить в БД — поэтому async и с ctx."""

    @classmethod
    @abstractmethod
    async def page_content(cls, ctx: BaseContext[Any], page: int) -> ViewContent:
        """Содержимое одной страницы, без навигационного ряда — его добавит render()."""

    @classmethod
    async def closed(cls, ctx: BaseContext[Any]) -> None:
        """Нажали "✕". По умолчанию удаляет сообщение; переопределите для другого."""
        await ctx.delete_message()

    @classmethod
    def _count(cls, total: int) -> int:
        return max(1, -(-total // cls.per_page))

    @classmethod
    async def render(cls, ctx: BaseContext[Any], data: CallbackPayload | None) -> ViewContent:
        requested = data.page if isinstance(data, cls.payload) else 0  # type: ignore[attr-defined]
        count = cls._count(await cls.total(ctx))
        page = max(0, min(requested, count - 1))
        content = await cls.page_content(ctx, page)

        # cls.payload тут всегда _Page (см. __init_subclass__) с полями action/page,
        # но статически известен только как базовый CallbackPayload — без полей.
        payload = cls.payload
        nav = [
            button("«", payload(page=page - 1))  # type: ignore[call-arg]
            if page > 0
            else button(" ", payload(action="noop")),  # type: ignore[call-arg]
            button(f"{page + 1}/{count}", payload(action="noop")),  # type: ignore[call-arg]
            button("»", payload(page=page + 1))  # type: ignore[call-arg]
            if page < count - 1
            else button(" ", payload(action="noop")),  # type: ignore[call-arg]
        ]
        if cls.closable:
            nav.append(button("✕", payload(action="close")))  # type: ignore[call-arg]

        return ViewContent(body=content.body, rows=[*content.rows, nav])

    @classmethod
    async def press(cls, ctx: BaseContext[Any]) -> None:
        data = cls.payload.try_unpack(ctx.callback_query.data or "")
        if data is None or data.action == "noop":  # type: ignore[attr-defined]
            await ctx.callback_query.answer()
            return
        if data.action == "close":  # type: ignore[attr-defined]
            await cls.closed(ctx)
            await ctx.callback_query.answer()
            return

        await super().press(ctx)
