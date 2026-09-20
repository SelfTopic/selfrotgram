import keyword
from dataclasses import dataclass, field
from pathlib import Path

from .templates import ENV_EXAMPLE, package_files


class InitError(Exception):
    """Команду нельзя выполнить: показывается пользователю без трейсбека."""


@dataclass
class InitResult:
    created: list[Path] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    module: str = ""  # как запускать: python -m <module>


def _check_path(path: Path) -> list[str]:
    parts = list(path.parts)
    if path.is_absolute() or not parts or ".." in parts:
        raise InitError(
            f"Путь {str(path)!r} должен быть относительным и внутри проекта"
        )

    for part in parts:
        if not part.isidentifier() or keyword.iskeyword(part):
            raise InitError(
                f"{part!r} нельзя использовать как имя пакета Python "
                "(буквы, цифры и подчёркивание, без дефисов)"
            )

    return parts


def init_project(
    root: Path, package: str = "src/bot", *, dry_run: bool = False
) -> InitResult:
    """
    Создаёт заготовку проекта. Существующие файлы не перезаписывает (пропускает).
    root — папка проекта, package — путь пакета бота относительно неё.
    """
    parts = _check_path(Path(package))
    result = InitResult(module=".".join(parts))

    files: dict[Path, str] = {root / ".env.example": ENV_EXAMPLE}
    for depth in range(1, len(parts)):  # src/__init__.py для src/bot
        files[root.joinpath(*parts[:depth], "__init__.py")] = ""
    for relative, content in package_files().items():
        files[root.joinpath(*parts, relative)] = content

    for target, content in files.items():
        if target.exists():
            result.skipped.append(target)
            continue

        result.created.append(target)
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

    return result
