import keyword
import re
from dataclasses import dataclass, field
from pathlib import Path

from .init import InitError
from .templates import ROUTER_FILE, ROUTER_PACKAGE

_NAME = re.compile(r"[a-z][a-z0-9_]*")
IMPORT_MARK = "# selfrot: imports"
ROUTERS_MARK = "# selfrot: routers"


@dataclass
class AddResult:
    created: list[Path] = field(default_factory=list)
    wired: bool = False  # подключён в RootRouter автоматически
    manual: list[str] = field(default_factory=list)  # строки для ручной вставки
    root_router: Path | None = None
    router_class: str = ""


def router_class_name(name: str) -> str:
    """user_stats -> UserStatsRouter."""
    return "".join(part.capitalize() for part in name.split("_")) + "Router"


def handler_class_name(name: str) -> str:
    return router_class_name(name).removesuffix("Router")


def _check_name(name: str) -> None:
    if not _NAME.fullmatch(name) or keyword.iskeyword(name):
        raise InitError(
            f"Имя роутера {name!r}: строчные латинские буквы, цифры и подчёркивание, "
            "с буквы (например profile или user_stats)"
        )


def wire_router(text: str, router: str, module: str) -> str | None:
    """
    Добавляет импорт и элемент кортежа в routers/__init__.py по меткам
    `# selfrot: imports` и `# selfrot: routers`. None: меток нет, править нечего.
    """
    lines = text.splitlines(keepends=True)
    imports_at = next(
        (i for i, l in enumerate(lines) if l.strip().startswith(IMPORT_MARK)), None
    )
    routers_at = next(
        (i for i, l in enumerate(lines) if l.strip().startswith(ROUTERS_MARK)), None
    )
    if imports_at is None or routers_at is None:
        return None

    indent = lines[routers_at][
        : len(lines[routers_at]) - len(lines[routers_at].lstrip())
    ]
    # Вставляем перед метками, поэтому порядок уже подключённых сохраняется.
    for index, line in sorted(
        [
            (imports_at, f"from .{module} import {router}\n"),
            (routers_at, f"{indent}{router},\n"),
        ],
        reverse=True,
    ):
        lines.insert(index, line)

    return "".join(lines)


def add_router(
    root: Path,
    name: str,
    package: str = "src/bot",
    *,
    module: bool = False,
    dry_run: bool = False,
) -> AddResult:
    """
    Создаёт роутер: файл routers/<name>.py или (module=True) папку routers/<name>/ с
    пустым роутером в __init__.py, и подключает его в RootRouter. Существующее не
    перезаписывает.
    """
    _check_name(name)
    routers_dir = root.joinpath(*Path(package).parts, "routers")
    root_router = routers_dir / "__init__.py"
    if not root_router.exists():
        raise InitError(
            f"Не найден {root_router.relative_to(root)}: сначала `selfrot init` "
            "(или укажите пакет бота через --package)"
        )

    file_target, folder_target = routers_dir / f"{name}.py", routers_dir / name
    if file_target.exists() or folder_target.exists():
        raise InitError(f"Роутер {name!r} уже существует, ничего не изменено")

    router = router_class_name(name)
    fields = {"name": name, "router": router, "handler": handler_class_name(name)}
    result = AddResult(root_router=root_router, router_class=router)
    if module:
        target, content = folder_target / "__init__.py", ROUTER_PACKAGE.format(**fields)
    else:
        target, content = file_target, ROUTER_FILE.format(**fields)

    result.created.append(target)
    wired = wire_router(root_router.read_text(encoding="utf-8"), router, name)
    if wired is None:
        result.manual = [
            f"from .{name} import {router}",
            f"routers = (..., {router})",
        ]
    else:
        result.wired = True

    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        if wired is not None:
            root_router.write_text(wired, encoding="utf-8")

    return result
