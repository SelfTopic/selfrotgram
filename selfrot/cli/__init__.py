import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .. import __version__
from .init import InitError, init_project


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _cmd_init(args: argparse.Namespace) -> int:
    root = Path.cwd()
    try:
        result = init_project(root, args.package, dry_run=args.dry_run)
    except InitError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    label = "Было бы создано" if args.dry_run else "Создано"
    if result.created:
        print(f"{label}:")
        for path in result.created:
            print(f"  + {_relative(path, root)}")
    if result.skipped:
        print("Уже есть, не тронуто:")
        for path in result.skipped:
            print(f"  = {_relative(path, root)}")
    if not result.created:
        print("Ничего не создано: всё уже на месте.")
        return 0

    if args.dry_run:
        return 0

    print(
        "\nДальше:\n"
        "  1. Скопируйте .env.example в .env и впишите BOT_TOKEN. Не коммитьте .env:\n"
        "     добавьте его в .gitignore.\n"
        f"  2. Запуск: BOT_TOKEN=... python -m {result.module}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="selfrot", description="Инструменты selfrotgram."
    )
    parser.add_argument(
        "--version", action="version", version=f"selfrotgram {__version__}"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser(
        "init",
        help="создать заготовку проекта в текущей папке",
        description=(
            "Создаёт пакет бота (по умолчанию src/bot): __main__.py с диспетчером, bot.py, "
            "context.py, routers/ со стартовым роутером и пустые keyboards/, middlewares/, "
            "filters/, а в текущей папке .env.example. Существующие файлы не перезаписывает."
        ),
    )
    init.add_argument(
        "package",
        nargs="?",
        default="src/bot",
        help="путь пакета бота относительно текущей папки (по умолчанию src/bot)",
    )
    init.add_argument(
        "--dry-run", action="store_true", help="только показать, что будет создано"
    )
    init.set_defaults(handler=_cmd_init)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.handler(args)
