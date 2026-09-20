import importlib
import inspect
import pkgutil
import sys
import traceback
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any

from ..dispatcher import BaseDispatcher
from ..handlers.base import BaseHandler
from ..router.base import BaseRouter
from .analysis import iter_handlers, iter_routers, unreachable
from .init import InitError, _check_path
from .tree import load_dispatcher


@dataclass
class Problem:
    level: str  # "error" | "warning"
    where: str  # модуль или «диспетчер»
    message: str
    details: str = ""  # трейсбек для -v


@dataclass
class Report:
    problems: list[Problem] = field(default_factory=list)
    modules: int = 0
    handlers: int = 0
    routers: int = 0

    @property
    def errors(self) -> list[Problem]:
        return [p for p in self.problems if p.level == "error"]

    @property
    def warnings(self) -> list[Problem]:
        return [p for p in self.problems if p.level == "warning"]

    def add(self, level: str, where: str, message: str, details: str = "") -> None:
        self.problems.append(Problem(level, where, message, details))


def _module_names(directory: Path, prefix: str) -> list[str]:
    """Модули пакета по файлам, без импорта: так одна ошибка не прячет остальные."""
    names: list[str] = []
    for info in pkgutil.iter_modules([str(directory)]):
        name = f"{prefix}.{info.name}"
        names.append(name)
        if info.ispkg:
            names += _module_names(directory / info.name, name)

    return names


def _own_classes(modules: list[ModuleType]) -> list[type]:
    """Классы, объявленные именно в этих модулях (а не импортированные в них)."""
    found: list[type] = []
    for module in modules:
        for value in vars(module).values():
            if inspect.isclass(value) and value.__module__ == module.__name__:
                found.append(value)

    return found


def _unused(candidates: list[type]) -> list[type]:
    """Без базовых: класс, от которого в проекте наследуют, подключать не нужно."""
    return [
        c
        for c in candidates
        if not any(o is not c and issubclass(o, c) for o in candidates)
    ]


def run_check(
    root: Path, package: str = "src/bot", target: str | None = None
) -> Report:
    parts = _check_path(Path(package))
    directory = root.joinpath(*parts)
    if not directory.is_dir():
        raise InitError(
            f"Нет папки {package}: выполните `selfrot init` или укажите пакет через --package"
        )

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    report = Report()
    name = ".".join(parts)
    loaded: list[ModuleType] = []
    for module_name in [name, *_module_names(directory, name)]:
        try:
            loaded.append(importlib.import_module(module_name))
        except (
            Exception,  # noqa: BLE001 - код пользователя: собираем все ошибки, не падаем
            SystemExit,
        ) as error:
            report.add(
                "error",
                module_name,
                f"{type(error).__name__}: {error}",
                traceback.format_exc(),
            )

    report.modules = len(loaded)

    try:
        dispatcher = load_dispatcher(target or f"{name}.__main__:Dispatcher", root)
    except InitError as error:
        report.add("error", "диспетчер", str(error))
        return report

    refs = list(iter_handlers(dispatcher))
    routers = list(iter_routers(dispatcher))
    report.handlers, report.routers = len(refs), len(routers) - 1

    if not refs:
        report.add(
            "warning", "диспетчер", "нет ни одного хендлера: бот ничего не обработает"
        )

    for index, reason in unreachable(refs).items():
        handler = refs[index].handler
        report.add(
            "warning", handler.__module__, f"{handler.__name__} недостижим: {reason}"
        )

    for handler, times in Counter(ref.handler for ref in refs).items():
        if times > 1:
            report.add(
                "warning",
                handler.__module__,
                f"{handler.__name__} подключён {times} раза",
            )

    own = _own_classes(loaded)
    registered_handlers = {ref.handler for ref in refs}
    handlers: list[type] = [
        c
        for c in own
        if issubclass(c, BaseHandler)
        and c is not BaseHandler
        and not inspect.isabstract(c)
        and hasattr(c, "update_field")
    ]
    for handler in _unused(handlers):
        if handler not in registered_handlers:
            report.add(
                "warning",
                handler.__module__,
                f"хендлер {handler.__name__} нигде не подключён: добавьте его в handlers роутера",
            )

    registered_routers: set[Any] = {type(router) for router in routers}
    router_classes: list[type] = [
        c
        for c in own
        if issubclass(c, BaseRouter) and not issubclass(c, BaseDispatcher)
    ]
    for router in _unused(router_classes):
        if router not in registered_routers:
            report.add(
                "warning",
                router.__module__,
                f"роутер {router.__name__} не подключён: добавьте его в routers родителя "
                "(или в кортеж RootRouter)",
            )

    return report


def plural(n: int, one: str, few: str, many: str) -> str:
    if 11 <= n % 100 <= 14:
        return f"{n} {many}"
    return f"{n} " + {1: one, 2: few, 3: few, 4: few}.get(n % 10, many)
