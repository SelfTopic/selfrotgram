from abc import ABC, abstractmethod
from typing import Any, Generic

from .context import TContext
from .exceptions import DefinitionError


class BaseTask(ABC, Generic[TContext]):
    """
    Фоновая периодическая задача — для работы, которая не ждёт апдейта, а идёт сама
    по расписанию (проверить просроченные браки, обновить кеш раз в сутки): Every(interval,
    ВашКласс) в Dispatcher.tasks.

        class MarriageExpiry(BaseTask[AppContext]):
            async def run(self) -> None:
                expired = await self.ctx.db.marriage.find_expired()
                for marriage in expired:
                    await self.ctx.db.marriage.dissolve(marriage)

        class Dispatcher(BaseDispatcher[AppContext]):
            tasks = (Every(30, MarriageExpiry),)

    self.ctx — такого же типа, что и у хендлеров, и так же прошедший мидлвари
    диспетчера (сессия БД, сервисы — всё работает так же, как в хендлере), только
    ctx.is_background = True: апдейта за этим вызовом нет, он не связан ни с чатом,
    ни с пользователем (ctx.chat, ctx.user и подобное — None, как у апдейта без
    этих полей).
    """

    ctx: TContext

    def __init__(self, ctx: TContext) -> None:
        self.ctx = ctx

    @abstractmethod
    async def run(self) -> None: ...

    async def on_error(self, exc: Exception) -> None:
        """
        Ошибка из run() (или из мидлварей диспетчера вокруг неё). Вернулся нормально —
        ошибка обработана. По умолчанию не обрабатывает и отдаёт выше, в on_error
        диспетчера: `raise exc`.
        """
        raise exc


class Every:
    """
    Every(30, MarriageExpiry) в Dispatcher.tasks: MarriageExpiry.run() раз в interval
    секунд, пока диспетчер работает (polling()/webhook()). Старт и остановка —
    забота диспетчера, отдельно запускать и глушить в __main__.py не нужно.
    """

    def __init__(self, interval: float, task: type[BaseTask[Any]]) -> None:
        if interval <= 0:
            raise DefinitionError(f"Every(interval={interval!r}): interval должен быть > 0")

        self.interval = interval
        self.task_cls = task

    def __repr__(self) -> str:
        return f"Every({self.interval}, {self.task_cls.__name__})"
