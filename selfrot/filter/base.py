from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any, ClassVar, Generic, TypeVar, cast

from pydantic import BaseModel

from ..context import BaseContext
from ..exceptions import DefinitionError
from ..utils.narrowing import required_fields, root_type

TContext = TypeVar("TContext", bound=BaseContext[Any])


@dataclass(frozen=True)
class Guarantee:
    """Что фильтр обещает про объект апдейта: тип Bot API (None — любой) и поля."""

    root: type[BaseModel] | None = None
    fields: frozenset[str] = frozenset()


def _merge_roots(
    left: type[BaseModel] | None,
    right: type[BaseModel] | None,
    description: str,
) -> type[BaseModel] | None:
    if left is None:
        return right
    if right is None or left is right:
        return left

    raise DefinitionError(
        f"{description}: фильтры для разных типов ({left.__name__} и {right.__name__})"
    )


def intersect_guarantees(guarantees: Iterable[Guarantee], description: str) -> Guarantee:
    """
    Пересечение нескольких гарантий: тип Bot API общий у всех, поля — только те, что
    гарантируют ВСЕ сразу, а не хотя бы одна (та же арифметика, что у `a | b` для двух
    фильтров, только для произвольного их числа — используется и там, и в проверке
    нескольких веток-методов одного хендлера, см. handlers/base.py).
    """
    root: type[BaseModel] | None = None
    fields: frozenset[str] | None = None
    for guarantee in guarantees:
        root = _merge_roots(root, guarantee.root, description)
        fields = guarantee.fields if fields is None else fields & guarantee.fields

    return Guarantee(root, fields if fields is not None else frozenset())


class BaseFilter(ABC, Generic[TContext]):
    """
    check() — обычная асинхронная проверка (никакой магии): фильтр может ходить в
    кеш/БД. Свой фильтр достаточно написать только с check(): по умолчанию он
    подходит любому виду обработчика и ничего не гарантирует.

    guarantees — суженный тип, поля которого check() уже проверил (TextMessage).
    Так делают Has*, Command и т. п. Комбинаторы считают гарантии сами:
    `a & b` — сумма, `a | b` — то, что обещают обе ветки, `~a` — ничего.
    Заголовок хендлера сверяется с итоговой гарантией при создании класса.

    narrow() — старый способ: cast контекста к суженному подклассу (нужен только
    для данных, которые кладут мидлвари, вроде ctx.db).
    """

    guarantees: ClassVar[type[BaseModel] | None] = None

    @abstractmethod
    async def check(self, ctx: BaseContext[Any]) -> bool: ...

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Фильтр как декоратор метода хендлера — ветка диспетчеризации внутри одного
        класса (см. handlers/base.py): `self.query` у класса остаётся None, методы
        перебираются по порядку, первый подошедший вызывается. Два декоратора на
        одном методе — DefinitionError, а не тихая перезапись: иначе непонятно, что
        вообще показывать в `selfrot tree`/`check`.
        """
        existing = getattr(func, "_query", None)
        if existing is not None:
            raise DefinitionError(
                f"{getattr(func, '__qualname__', func)}: два декоратора-фильтра на "
                f"одном методе ({existing!r} и {self!r})"
            )

        func._query = self  # type: ignore[attr-defined]
        return func

    def guarantee(self) -> Guarantee:
        if self.guarantees is None:
            return Guarantee()

        return Guarantee(root_type(self.guarantees), required_fields(self.guarantees))

    def narrow(self, ctx: BaseContext[Any]) -> TContext:
        return cast(TContext, ctx)

    def __and__(self, other: "BaseFilter[Any]") -> "AndFilter":
        return AndFilter(self, other)

    def __or__(self, other: "BaseFilter[Any]") -> "OrFilter":
        return OrFilter(self, other)

    def __invert__(self) -> "NotFilter":
        return NotFilter(self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"


class AndFilter(BaseFilter[BaseContext[Any]]):
    """Оба фильтра, слева направо: правый не вызывается, если левый сказал нет."""

    def __init__(self, left: BaseFilter[Any], right: BaseFilter[Any]) -> None:
        self.left = left
        self.right = right

        a, b = left.guarantee(), right.guarantee()
        self._guarantee = Guarantee(
            _merge_roots(a.root, b.root, repr(self)), a.fields | b.fields
        )

    async def check(self, ctx: BaseContext[Any]) -> bool:
        return await self.left.check(ctx) and await self.right.check(ctx)

    def guarantee(self) -> Guarantee:
        return self._guarantee

    def narrow(self, ctx: BaseContext[Any]) -> BaseContext[Any]:
        return ctx

    def __repr__(self) -> str:
        return f"({self.left!r} & {self.right!r})"


class OrFilter(BaseFilter[BaseContext[Any]]):
    """Любой из двух, слева направо: правый не вызывается, если левый сказал да."""

    def __init__(self, left: BaseFilter[Any], right: BaseFilter[Any]) -> None:
        self.left = left
        self.right = right

        self._guarantee = intersect_guarantees(
            (left.guarantee(), right.guarantee()), repr(self)
        )

    async def check(self, ctx: BaseContext[Any]) -> bool:
        return await self.left.check(ctx) or await self.right.check(ctx)

    def guarantee(self) -> Guarantee:
        return self._guarantee

    def narrow(self, ctx: BaseContext[Any]) -> BaseContext[Any]:
        return ctx

    def __repr__(self) -> str:
        return f"({self.left!r} | {self.right!r})"


class NotFilter(BaseFilter[BaseContext[Any]]):
    """Отрицание: про объект ничего не гарантирует (кроме его типа Bot API)."""

    def __init__(self, inner: BaseFilter[Any]) -> None:
        self.inner = inner

    async def check(self, ctx: BaseContext[Any]) -> bool:
        return not await self.inner.check(ctx)

    def guarantee(self) -> Guarantee:
        return Guarantee(self.inner.guarantee().root)

    def narrow(self, ctx: BaseContext[Any]) -> BaseContext[Any]:
        return ctx

    def __repr__(self) -> str:
        return f"~{self.inner!r}"
