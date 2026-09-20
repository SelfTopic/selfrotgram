from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

from ..filter.base import AndFilter, BaseFilter, NotFilter, OrFilter
from ..handlers.base import BaseHandler
from ..router.base import BaseRouter


@dataclass(frozen=True)
class HandlerRef:
    """Хендлер и роутер, в котором он стоит."""

    handler: type[BaseHandler[Any]]
    router: BaseRouter[Any]


def iter_handlers(root: BaseRouter[Any]) -> Iterator[HandlerRef]:
    """Хендлеры в порядке проверки диспетчером: свои, затем вложенные роутеры вглубь."""
    for handler in root.handlers:
        yield HandlerRef(handler, root)
    for child in root.children:
        yield from iter_handlers(child)


def iter_routers(root: BaseRouter[Any]) -> Iterator[BaseRouter[Any]]:
    yield root
    for child in root.children:
        yield from iter_routers(child)


def _faithful(query: BaseFilter[Any]) -> bool:
    """
    Можно ли по repr узнать, что делает фильтр. Встроенные фильтры печатают все свои
    параметры; у пользовательских repr по умолчанию `Имя()` и скрывает параметры.
    """
    if isinstance(query, (AndFilter, OrFilter)):
        return _faithful(query.left) and _faithful(query.right)
    if isinstance(query, NotFilter):
        return _faithful(query.inner)

    return type(query).__module__.startswith("selfrot.")


def same_filter(a: BaseFilter[Any], b: BaseFilter[Any]) -> bool:
    """Одинаковые фильтры: тогда второй хендлер никогда не получит апдейт."""
    if (
        not (_faithful(a) and _faithful(b))
        or type(a) is not type(b)
        or repr(a) != repr(b)
    ):
        return False

    # Имя класса в repr не различает одноимённые классы из разных модулей.
    for attr in ("payload", "args_model"):
        if getattr(a, attr, None) is not getattr(b, attr, None):
            return False

    return True


def unreachable(refs: list[HandlerRef]) -> dict[int, str]:
    """
    Индекс хендлера (в порядке проверки) -> почему он никогда не сработает:
    выше стоит хендлер того же вида апдейта без фильтра или с тем же фильтром.
    """
    reasons: dict[int, str] = {}
    catch_all: dict[str, str] = {}
    seen: dict[str, list[tuple[BaseFilter[Any], str]]] = {}

    for index, ref in enumerate(refs):
        handler = ref.handler
        kind = handler.update_field
        if above := catch_all.get(kind):
            reasons[index] = f"выше {above} без фильтра ловит всё этого вида"
        elif handler.query is not None:
            for query, name in seen.get(kind, []):
                if same_filter(query, handler.query):
                    reasons[index] = f"выше {name} тот же фильтр {handler.query!r}"
                    break

        if handler.query is None:
            catch_all.setdefault(kind, handler.__name__)
        else:
            seen.setdefault(kind, []).append((handler.query, handler.__name__))

    return reasons
