import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class StoredState:
    """Что лежит в хранилище: имя состояния и его данные (JSON-совместимый словарь)."""

    name: str
    data: dict[str, Any] | None = None


class Storage(Protocol):
    """
    Хранилище состояний. Ключ — строка (у Redis и SQL — как есть), поэтому своё
    хранилище пишется тремя методами.
    """

    async def load(self, key: str) -> StoredState | None: ...

    async def save(self, key: str, stored: StoredState) -> None: ...

    async def delete(self, key: str) -> None: ...


class MemoryStorage:
    """
    В памяти процесса: после перезапуска состояния пропадают. ttl — сколько секунд
    живёт состояние без обращений (скользящее окно: каждое set() продлевает).
    Диалог, который бросили, исчезает сам, и `InState` для него перестаёт совпадать.
    """

    def __init__(
        self, ttl: float | None = None, *, clock: Callable[[], float] = time.monotonic
    ) -> None:
        self.ttl = ttl
        self._clock = clock
        self._items: dict[str, tuple[StoredState, float | None]] = {}
        self._last_sweep = clock()

    async def load(self, key: str) -> StoredState | None:
        item = self._items.get(key)
        if item is None:
            return None

        stored, expires = item
        if expires is not None and self._clock() >= expires:
            del self._items[key]
            return None

        return stored

    async def save(self, key: str, stored: StoredState) -> None:
        now = self._clock()
        self._items[key] = (stored, None if self.ttl is None else now + self.ttl)
        self._sweep(now)

    async def delete(self, key: str) -> None:
        self._items.pop(key, None)

    def _sweep(self, now: float) -> None:
        # Забытые диалоги, к которым никто не вернулся, иначе копились бы вечно.
        if self.ttl is None or now - self._last_sweep < self.ttl:
            return

        self._last_sweep = now
        expired = [k for k, (_, e) in self._items.items() if e is not None and now >= e]
        for key in expired:
            del self._items[key]

    def __len__(self) -> int:
        return len(self._items)
