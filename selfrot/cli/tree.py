import importlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..filter.base import AndFilter, BaseFilter, NotFilter, OrFilter
from ..filter.command import AnyCommand
from ..handlers.base import BaseHandler, _header_payload_type
from ..router.base import BaseRouter
from .analysis import chain, iter_handlers, unreachable
from .init import InitError

# Токен нужен только конструктору Bot, в сеть при построении дерева никто не ходит.
DUMMY_TOKEN = "0:selfrot-tree"
_OVERRIDES = ("pre_handle", "after_handle", "on_error")
# Длиннее — цепочка &/| переносится на несколько строк (без учёта отступа строки в дереве).
_MAX_INLINE = 72


@dataclass
class Row:
    left: str  # ветки дерева и имя
    kind: str = ""
    filter: str = ""  # может быть в несколько строк (AnyCommand)
    note: str = ""
    cont: str = ""  # ветки дерева для продолжения фильтра на следующих строках


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


def _nested(text: str) -> str:
    """Строки блока, вложенного на один уровень глубже: каждая сдвигается ещё на 4."""
    return text.replace("\n", "\n    ")


def _block(items: list[str]) -> str:
    """AnyCommand(\n    x,\n    y,\n)."""
    body = "".join(f"    {_nested(item)},\n" for item in items)
    return f"AnyCommand(\n{body})"


def _combine(sign: str, parts: list[str]) -> str:
    """
    (a & b & c) на одной строке, а если длинно или в частях уже есть перенос — по одному
    операнду на строку.
    """
    flat = f" {sign} ".join(parts)
    if "\n" not in flat and len(flat) <= _MAX_INLINE:
        return f"({flat})"

    lines = [f"(\n    {_nested(parts[0])}"]
    lines += [f"    {sign} {_nested(part)}" for part in parts[1:]]
    lines.append(")")
    return "\n".join(lines)


def _pretty(query: BaseFilter[Any]) -> str:
    """repr, но длинные AnyCommand и цепочки &/| раскладываются по строкам, как в коде."""
    if isinstance(query, AnyCommand):
        return _block([repr(command) for command in query.commands])
    if isinstance(query, (AndFilter, OrFilter)):
        sign = "&" if isinstance(query, AndFilter) else "|"
        parts = [_pretty(part) for part in chain(query, type(query))]
        return _combine(sign, parts)
    if isinstance(query, NotFilter):
        return f"~{_pretty(query.inner)}"

    return repr(query)


def _filter_text(handler: type[BaseHandler[Any]]) -> str:
    query = handler.query
    return _pretty(query) if query is not None else "без фильтра: ловит всё этого вида"


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
                    next_prefix,
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
            head = f"{row.left.ljust(left_width)}  {row.kind.ljust(kind_width)}  "
            first, *rest = row.filter.split("\n")
            # Продолжение фильтра идёт под ним; слева остаются только ветки дерева.
            lines.append((head + first).rstrip())
            lines += [(row.cont.ljust(len(head)) + line).rstrip() for line in rest]
            if row.note:
                lines[-1] += f"  {row.note}"
            continue

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
