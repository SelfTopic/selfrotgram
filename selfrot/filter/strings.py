import re
from abc import abstractmethod
from typing import Any

from ..context import BaseContext
from ..exceptions import FilterMatchError
from .base import BaseFilter


class StringFilter(BaseFilter[Any]):
    """
    Фильтр по строке из апдейта. Подкласс отвечает на два вопроса: откуда взять
    строку (_read: текст сообщения, data кнопки) и как её проверить (_test).
    Источник и способ сравнения собираются наследованием, см. text.py и callback.py.
    """

    @abstractmethod
    def _read(self, ctx: BaseContext[Any]) -> str | None: ...

    @abstractmethod
    def _test(self, value: str) -> bool: ...

    async def check(self, ctx: BaseContext[Any]) -> bool:
        value = self._read(ctx)
        return value is not None and self._test(value)


class Compare(StringFilter):
    """Сравнение с образцом; ignore_case=True сравнивает через casefold()."""

    def __init__(self, value: str, *, ignore_case: bool = False) -> None:
        self.value = value
        self.ignore_case = ignore_case
        self._sample = self._fold(value)

    def _fold(self, text: str) -> str:
        return text.casefold() if self.ignore_case else text

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value!r})"


class Equals(Compare):
    def _test(self, value: str) -> bool:
        return self._fold(value) == self._sample


class Startswith(Compare):
    def _test(self, value: str) -> bool:
        return self._fold(value).startswith(self._sample)


class Endswith(Compare):
    def _test(self, value: str) -> bool:
        return self._fold(value).endswith(self._sample)


class Contains(Compare):
    def _test(self, value: str) -> bool:
        return self._sample in self._fold(value)


class Regexp(StringFilter):
    """
    Регулярное выражение. По умолчанию re.match (совпадение с начала строки),
    full=True — re.fullmatch.

    Фильтр общий для всех апдейтов, поэтому результат в нём не хранится: в
    хендлере (например, в pre_handle) его берут явно, через match(ctx).
    """

    def __init__(
        self, pattern: str | re.Pattern[str], flags: int = 0, *, full: bool = False
    ) -> None:
        self.pattern = re.compile(pattern, flags)
        self.full = full

    def _find(self, value: str) -> re.Match[str] | None:
        if self.full:
            return self.pattern.fullmatch(value)

        return self.pattern.match(value)

    def _test(self, value: str) -> bool:
        return self._find(value) is not None

    def match(self, ctx: BaseContext[Any]) -> re.Match[str]:
        """Совпадение для этого апдейта. Только после того, как check() сказал да."""
        value = self._read(ctx)
        found = self._find(value) if value is not None else None
        if found is None:
            raise FilterMatchError(f"{self!r} не подошёл к этому апдейту")

        return found

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.pattern.pattern!r})"
