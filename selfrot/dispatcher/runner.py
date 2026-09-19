import asyncio
from collections.abc import Awaitable, Callable, Hashable


class UpdateRunner:
    """
    Запускает обработку апдейтов параллельно:

    - не больше `limit` одновременно; когда лимит выбран, submit() ждёт, то есть
      диспетчер перестаёт забирать новые апдейты (задачи не копятся без границы);
    - апдейты с одним ключом идут строго друг за другом, в порядке получения, а
      разные ключи — независимо. key=None — без порядка;
    - drain() при остановке даёт начатым обработчикам закончить, потом отменяет.

    Ошибки хендлеров здесь не обрабатываются: work должен ловить их сам.
    """

    def __init__(self, limit: int, shutdown_timeout: float) -> None:
        if limit < 1:
            raise ValueError("limit должен быть не меньше 1")

        self._slots = asyncio.Semaphore(limit)
        self._shutdown_timeout = shutdown_timeout
        # Ссылки нужны: цикл событий хранит задачи слабо, и сборщик мусора может
        # убить задачу посреди хендлера.
        self._tasks: set[asyncio.Task[None]] = set()
        self._tails: dict[Hashable, asyncio.Task[None]] = {}

    @property
    def active(self) -> int:
        return len(self._tasks)

    async def submit(
        self, key: Hashable | None, work: Callable[[], Awaitable[None]]
    ) -> None:
        await self._slots.acquire()
        self._start(key, work)

    async def try_submit(
        self, key: Hashable | None, work: Callable[[], Awaitable[None]]
    ) -> bool:
        """Как submit, но без ожидания: False, если свободных слотов нет."""
        if self._slots.locked():
            return False

        # Слот свободен, поэтому acquire() возвращается сразу, не отдавая управление:
        # между проверкой и захватом никто чужой не успеет занять слот.
        await self._slots.acquire()
        self._start(key, work)
        return True

    def _start(self, key: Hashable | None, work: Callable[[], Awaitable[None]]) -> None:
        previous = self._tails.get(key) if key is not None else None
        task = asyncio.create_task(self._run(previous, work))
        self._tasks.add(task)
        if key is not None:
            self._tails[key] = task

        task.add_done_callback(lambda done: self._finished(key, done))

    async def _run(
        self,
        previous: asyncio.Task[None] | None,
        work: Callable[[], Awaitable[None]],
    ) -> None:
        if previous is not None:
            # wait() не бросает чужую ошибку и не отменяет предыдущую задачу,
            # если отменили эту.
            await asyncio.wait([previous])

        await work()

    def _finished(self, key: Hashable | None, task: asyncio.Task[None]) -> None:
        self._slots.release()
        self._tasks.discard(task)
        if key is not None and self._tails.get(key) is task:
            del self._tails[key]

        if not task.cancelled():
            task.exception()  # прочитать, чтобы asyncio не жаловался в лог

    async def drain(self) -> None:
        pending = set(self._tasks)
        if not pending:
            return

        _, unfinished = await asyncio.wait(pending, timeout=self._shutdown_timeout)
        for task in unfinished:
            task.cancel()

        if unfinished:
            # Отмена доходит до хендлеров, и их post_handle успевает отработать.
            await asyncio.wait(unfinished)
