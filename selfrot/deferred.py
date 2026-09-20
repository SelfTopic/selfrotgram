import asyncio
import contextvars
import logging
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from .exceptions import DeferredLimitError

if TYPE_CHECKING:
    from .context import BaseContext
    from .handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class Deferred:
    """
    Отложенный вызов: ctx.defer(...) или self.defer(...) в хендлере. Пока хендлер не
    закончился, вызов только записан; стартует он после закрытия хендлера и мидлварей.
    Ручка нужна, чтобы отменить: `handle.cancel()`.
    """

    def __init__(
        self,
        fn: Callable[..., Awaitable[Any]],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        delay: float,
        ctx: "BaseContext[Any]",
        owner: "BaseHandler[Any] | None" = None,
    ) -> None:
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.delay = delay
        self.ctx = ctx
        self.owner = owner  # хендлер, чей on_error получит ошибку отложенного вызова
        self._task: asyncio.Task[None] | None = None
        self._cancelled = False
        self._finished = False
        self._delay_done = delay <= 0
        self._release: Callable[[], None] | None = None

    @property
    def cancelled(self) -> bool:
        return self._cancelled

    @property
    def done(self) -> bool:
        return self._finished

    @property
    def sleeping(self) -> bool:
        """Ещё ждёт свой delay."""
        return not self._delay_done and not self._finished

    def cancel(self) -> None:
        """Отменить: до старта вызов не состоится, во время задержки или работы прервётся."""
        if self._finished:
            return

        self._cancelled = True
        if self._task is not None:
            self._task.cancel()
        else:
            self._finish()

    def _finish(self) -> None:
        if self._finished:
            return

        self._finished = True
        if self._release is not None:
            self._release()


class BackgroundTasks:
    """
    Отложенные вызовы диспетчера: одна задача asyncio на вызов, которая спит delay и
    выполняет функцию. Хранит ссылки (иначе сборщик мусора мог бы убить задачу),
    считает вызовы (лимит) и при остановке отменяет спящие, а идущие дожидается.
    """

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self._count = 0
        self._items: set[Deferred] = set()

    @property
    def active(self) -> int:
        return self._count

    def register(self, deferred: Deferred) -> None:
        """Занять место под вызов; DeferredLimitError, если место кончилось."""
        if self._count >= self.limit:
            raise DeferredLimitError(
                f"Отложенных вызовов уже {self._count} (лимит {self.limit}): "
                "подождите или увеличьте Dispatcher.max_deferred"
            )

        self._count += 1
        deferred._release = self._release_one

    def _release_one(self) -> None:
        self._count -= 1

    def start(
        self,
        deferred: Deferred,
        on_error: Callable[[Deferred, Exception], Awaitable[None]],
    ) -> None:
        if deferred.cancelled:
            return

        # Чистый контекст: ContextVar хендлера (сессия БД) к этому моменту закрыт,
        # и видеть его отложенный вызов не должен.
        task = asyncio.create_task(
            self._run(deferred, on_error), context=contextvars.Context()
        )
        deferred._task = task
        self._items.add(deferred)
        task.add_done_callback(lambda _t, d=deferred: self._done(d))

    def discard(self, deferreds: list[Deferred]) -> None:
        """Хендлер не отработал успешно: записанные вызовы не запускаются."""
        for deferred in deferreds:
            deferred.cancel()

    def _done(self, deferred: Deferred) -> None:
        self._items.discard(deferred)
        deferred._finish()

    async def _run(
        self,
        deferred: Deferred,
        on_error: Callable[[Deferred, Exception], Awaitable[None]],
    ) -> None:
        try:
            if deferred.delay > 0:
                await asyncio.sleep(deferred.delay)
                deferred._delay_done = True

            await deferred.fn(*deferred.args, **deferred.kwargs)
        except Exception as exc:  # noqa: BLE001 - граница отложенного вызова
            try:
                await on_error(deferred, exc)
            except Exception:
                logger.exception(
                    "Ошибка отложенного вызова %r не разобрана", deferred.fn
                )

    async def drain(self, timeout: float) -> None:
        """Спящие таймеры отменить сразу, идущие вызовы дождаться до timeout, потом отменить."""
        items = list(self._items)
        for deferred in items:
            if deferred.sleeping:
                deferred.cancel()

        running = [d._task for d in items if d._task is not None and not d.sleeping]
        running = [t for t in running if not t.done()]
        if running:
            _, unfinished = await asyncio.wait(running, timeout=timeout)
            for task in unfinished:
                task.cancel()

        tasks = [d._task for d in items if d._task is not None]
        if tasks:
            await asyncio.wait(tasks)
