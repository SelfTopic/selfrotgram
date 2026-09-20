import importlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..handlers.base import BaseHandler, _header_payload_type
from ..router.base import BaseRouter
from .analysis import iter_handlers, unreachable
from .init import InitError

# Токен нужен только конструктору Bot, в сеть при построении дерева никто не ходит.
DUMMY_TOKEN = "0:selfrot-tree"
_OVERRIDES = ("pre_handle", "after_handle", "on_error")


@dataclass
class Row:
    left: str  # ветки дерева и имя
    kind: str = ""
    filter: str = ""
    note: str = ""


@dataclass
class Tree:
    rows: list[Row]
    routers: int
    handlers: int
    update_types: list[str]
    warnings: int


def load_dispatcher(target: str, root: Path) -> BaseRouter[Any]:
    """target: «src.bot.__main__:Dispatcher»; класс без двоеточия берётся как Dispatcher."""
    module_name, _, attr = target.partition(":")
    attr = attr or "Dispatcher"
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    try:
        module = importlib.import_module(module_name)
    except ImportError as error:
        raise InitError(f"Не удалось импортировать {module_name}: {error}") from error

    try:
        dispatcher_class = getattr(module, attr)
    except AttributeError as error:
        raise InitError(f"В {module_name} нет {attr}") from error

    try:
        return dispatcher_class(token=DUMMY_TOKEN)
    except Exception as error:  # код пользователя: показываем причину, а не трейсбек
        raise InitError(
            f"Не удалось создать {attr}: {type(error).__name__}: {error}"
        ) from error


def _filter_text(handler: type[BaseHandler[Any]]) -> str:
    query = handler.query
    return repr(query) if query is not None else "без фильтра: ловит всё этого вида"


def _kind_text(handler: type[BaseHandler[Any]]) -> str:
    promised = _header_payload_type(handler)
    return (
        f"{handler.update_field}: {promised.__name__}"
        if promised
        else handler.update_field
    )


def _overrides(handler: type[BaseHandler[Any]]) -> list[str]:
    return [
        name
        for name in _OVERRIDES
        if getattr(handler, name) is not getattr(BaseHandler, name)
    ]


def build_tree(
    dispatcher: BaseRouter[Any], *, verbose: bool = False, ascii_only: bool = False
) -> Tree:
    branch, last, pipe, blank = (
        ("|- ", "`- ", "|  ", "   ") if ascii_only else ("├─ ", "└─ ", "│  ", "   ")
    )
    rows: list[Row] = []
    counts = {"routers": 0, "handlers": 0, "warnings": 0}
    reasons = unreachable(list(iter_handlers(dispatcher)))

    def router_note(router: BaseRouter[Any]) -> str:
        names = ", ".join(m.__name__ for m in router.middlewares)
        return f"мидлвари: {names}" if names else ""

    def walk(router: BaseRouter[Any], prefix: str) -> None:
        items: list[Any] = [*router.handlers, *router.children]
        for index, item in enumerate(items):
            is_last = index == len(items) - 1
            left = prefix + (last if is_last else branch)
            next_prefix = prefix + (blank if is_last else pipe)

            if isinstance(item, BaseRouter):
                counts["routers"] += 1
                rows.append(Row(left + type(item).__name__, note=router_note(item)))
                walk(item, next_prefix)
                continue

            counts["handlers"] += 1
            notes: list[str] = []
            # Номер в порядке проверки: обход тот же, что у iter_handlers.
            if reason := reasons.get(counts["handlers"] - 1):
                counts["warnings"] += 1
                notes.append(f"! недостижим: {reason}")
            if verbose:
                if overrides := _overrides(item):
                    notes.append("переопределено: " + ", ".join(overrides))
                if doc := (item.__doc__ or "").strip().splitlines():
                    notes.append(doc[0].strip())

            rows.append(
                Row(
                    left + item.__name__,
                    _kind_text(item),
                    _filter_text(item),
                    "  ".join(notes),
                )
            )

    note = router_note(dispatcher)
    rows.append(Row(type(dispatcher).__name__, note=note))
    walk(dispatcher, "")
    types = sorted(dispatcher.used_update_types())
    return Tree(rows, counts["routers"], counts["handlers"], types, counts["warnings"])


def render(tree: Tree) -> str:
    handlers = [r for r in tree.rows if r.kind]
    left_width = max((len(r.left) for r in tree.rows), default=0)
    kind_width = max((len(r.kind) for r in handlers), default=0)
    lines = []
    for row in tree.rows:
        if row.kind:
            line = f"{row.left.ljust(left_width)}  {row.kind.ljust(kind_width)}  {row.filter}"
            line += f"  {row.note}" if row.note else ""
        else:
            line = row.left + (f"  ({row.note})" if row.note else "")
        lines.append(line.rstrip())

    updates = ", ".join(tree.update_types) or "нет"
    lines.append("")
    lines.append(
        f"Роутеров: {tree.routers} (без корня), хендлеров: {tree.handlers}. "
        f"allowed_updates: {updates}"
    )
    if tree.warnings:
        lines.append(f"Предупреждений: {tree.warnings}")
    return "\n".join(lines)
