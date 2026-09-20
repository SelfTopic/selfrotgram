import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .. import __version__
from .add import add_router
from .check import plural, run_check
from .init import InitError, init_project
from .tree import build_tree, load_dispatcher, render


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


def _cmd_add_router(args: argparse.Namespace) -> int:
    root = Path.cwd()
    try:
        result = add_router(
            root, args.name, args.package, module=args.module, dry_run=args.dry_run
        )
    except InitError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    dry = args.dry_run
    for path in result.created:
        print(f"{'Было бы создано' if dry else 'Создано'}: {_relative(path, root)}")

    root_router = _relative(result.root_router, root) if result.root_router else ""
    if result.wired:
        print(
            f"{'Было бы подключено' if dry else 'Подключено'} в {root_router}: {result.router_class}"
        )
    else:
        print(
            f"Меток `# selfrot: imports` и `# selfrot: routers` в {root_router} нет, "
            "подключите роутер вручную:"
        )
        for line in result.manual:
            print(f"  {line}")

    if args.module and not dry:
        print("Хендлеры кладите модулями рядом с __init__.py и добавляйте в handlers.")
    return 0


def _cmd_tree(args: argparse.Namespace) -> int:
    root = Path.cwd()
    target = args.target or ".".join(Path(args.package).parts) + ".__main__:Dispatcher"
    try:
        dispatcher = load_dispatcher(target, root)
    except InitError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    tree = build_tree(dispatcher, verbose=args.verbose, ascii_only=args.ascii)
    try:
        print(render(tree))
    except UnicodeEncodeError:
        print(render(build_tree(dispatcher, verbose=args.verbose, ascii_only=True)))
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    try:
        report = run_check(Path.cwd(), args.package, args.target)
    except InitError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    print(
        f"Проверка {args.package}: модулей {report.modules}, "
        f"роутеров {report.routers}, хендлеров {report.handlers}."
    )
    for problem in report.problems:
        label = "ошибка" if problem.level == "error" else "предупреждение"
        print(f"{label}: {problem.where}: {problem.message}")
        if args.verbose and problem.details:
            print(problem.details.rstrip())

    errors, warnings = len(report.errors), len(report.warnings)
    if not report.problems:
        print("Проблем не найдено.")
    else:
        print(
            "Итог: "
            + plural(errors, "ошибка", "ошибки", "ошибок")
            + ", "
            + plural(warnings, "предупреждение", "предупреждения", "предупреждений")
            + "."
        )

    return 1 if errors or (args.strict and warnings) else 0


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

    tree = commands.add_parser(
        "tree",
        help="показать роутеры, хендлеры и их фильтры",
        description=(
            "Строит диспетчер проекта (без сети и токена) и печатает дерево: роутеры с их "
            "мидлварями, хендлеры с видом апдейта, обещанным типом и фильтром. Сверху вниз "
            "это порядок проверки: побеждает первый подошедший хендлер. Хендлер без фильтра "
            "ловит всё своего вида, и последующие того же вида помечаются как недостижимые."
        ),
    )
    tree.add_argument(
        "target",
        nargs="?",
        help="модуль:класс диспетчера (по умолчанию <пакет>.__main__:Dispatcher)",
    )
    tree.add_argument(
        "--package", default="src/bot", help="путь пакета бота (по умолчанию src/bot)"
    )
    tree.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="добавить переопределённые методы и описания",
    )
    tree.add_argument(
        "--ascii", action="store_true", help="рисовать ветки обычными символами"
    )
    tree.set_defaults(handler=_cmd_tree)

    check = commands.add_parser(
        "check",
        help="проверить проект: ошибки описания и забытые подключения",
        description=(
            "Импортирует каждый модуль пакета (ошибки собираются все, а не только первая), "
            "собирает диспетчер и ищет то, что при запуске не видно: хендлер или роутер, "
            "который нигде не подключён, недостижимые хендлеры, один и тот же хендлер "
            "в двух местах. Ошибки дают код выхода 1; предупреждения только с --strict."
        ),
    )
    check.add_argument(
        "target",
        nargs="?",
        help="модуль:класс диспетчера (по умолчанию <пакет>.__main__:Dispatcher)",
    )
    check.add_argument(
        "--package", default="src/bot", help="путь пакета бота (по умолчанию src/bot)"
    )
    check.add_argument(
        "--strict", action="store_true", help="считать предупреждения ошибками (для CI)"
    )
    check.add_argument(
        "-v", "--verbose", action="store_true", help="показать трейсбеки ошибок импорта"
    )
    check.set_defaults(handler=_cmd_check)

    add = commands.add_parser("add", help="добавить в проект новую часть")
    kinds = add.add_subparsers(dest="kind", required=True)
    router = kinds.add_parser(
        "router",
        help="создать роутер и подключить его в RootRouter",
        description=(
            "Создаёт routers/<имя>.py с примером хендлера и подключает роутер в "
            "routers/__init__.py по меткам `# selfrot: imports` и `# selfrot: routers`. "
            "С --module создаёт не файл, а папку routers/<имя>/ с пустым роутером в "
            "__init__.py, готовым принимать хендлеры. Существующее не перезаписывает."
        ),
    )
    router.add_argument("name", help="имя роутера: profile, user_stats")
    router.add_argument(
        "--module",
        action="store_true",
        help="создать роутер папкой, а не файлом",
    )
    router.add_argument(
        "--package", default="src/bot", help="путь пакета бота (по умолчанию src/bot)"
    )
    router.add_argument(
        "--dry-run", action="store_true", help="только показать, что будет сделано"
    )
    router.set_defaults(handler=_cmd_add_router)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.handler(args)
