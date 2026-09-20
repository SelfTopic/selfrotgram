import os
import subprocess
import sys
from pathlib import Path

import pytest

from selfrot.cli import main
from selfrot.cli.add import add_router
from selfrot.cli.check import plural, run_check
from selfrot.cli.init import InitError, init_project

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def bot_project(project: Path) -> Path:
    init_project(project)
    return project


def write(root: Path, relative: str, text: str) -> None:
    (root / "src/bot" / relative).write_text(text, encoding="utf-8")


HEAD = (
    "from selfrot import BaseRouter, MessageHandler\n"
    "from selfrot.filter import Command, Text\n"
    "from selfrot.types import TextMessage\n\n"
    "from ..context import AppContext\n\n\n"
)


def messages(report, level: str | None = None) -> list[str]:
    return [p.message for p in report.problems if level is None or p.level == level]


class TestCleanProject:
    def test_fresh_project_has_no_problems(self, bot_project):
        report = run_check(bot_project)
        assert report.problems == []
        assert (report.handlers, report.routers) == (1, 2)

    def test_added_routers_are_fine(self, bot_project):
        add_router(bot_project, "profile")
        add_router(bot_project, "shop", module=True)
        assert run_check(bot_project).problems == []


class TestImportErrors:
    def test_all_errors_are_collected_not_only_the_first(self, bot_project):
        write(bot_project, "filters/oops.py", "import nonexistent_thing\n")
        write(
            bot_project,
            "routers/broken.py",
            HEAD
            + "class NoGuarantee(MessageHandler[AppContext[TextMessage]]):\n    async def handle(self): ...\n",
        )
        write(bot_project, "keyboards/syntax.py", "def broken(:\n")

        report = run_check(bot_project)
        errors = {p.where: p.message for p in report.problems if p.level == "error"}
        assert "ModuleNotFoundError" in errors["src.bot.filters.oops"]
        assert "не гарантирует поля: text" in errors["src.bot.routers.broken"]
        assert "SyntaxError" in errors["src.bot.keyboards.syntax"]
        assert len(errors) == 3

    def test_a_module_that_exits_is_reported(self, bot_project):
        write(bot_project, "middlewares/exit.py", "raise SystemExit('стоп')\n")
        assert any("SystemExit" in m for m in messages(run_check(bot_project), "error"))

    def test_traceback_is_kept_for_verbose(self, bot_project):
        write(bot_project, "filters/oops.py", "import nonexistent_thing\n")
        problem = run_check(bot_project).errors[0]
        assert "Traceback" in problem.details

    def test_broken_dispatcher_is_reported_and_stops_analysis(self, bot_project):
        main_file = bot_project / "src/bot/__main__.py"
        main_file.write_text(
            main_file.read_text(encoding="utf-8").replace(
                "routers = (RootRouter,)",
                'routers = (RootRouter,)\n    auto_connect = (".nowhere",)',
            ),
            encoding="utf-8",
        )
        report = run_check(bot_project)
        assert any(
            "Не удалось создать Dispatcher" in m for m in messages(report, "error")
        )


class TestWarnings:
    def test_handler_not_registered_anywhere(self, bot_project):
        write(
            bot_project,
            "routers/start.py",
            (bot_project / "src/bot/routers/start.py").read_text(encoding="utf-8")
            + "\n\nclass Forgotten(MessageHandler[AppContext[TextMessage]]):\n"
            '    query = Command("forgotten")\n\n    async def handle(self): ...\n',
        )
        report = run_check(bot_project)
        assert any(
            "хендлер Forgotten нигде не подключён" in m
            for m in messages(report, "warning")
        )

    def test_router_not_connected(self, bot_project):
        write(
            bot_project,
            "routers/lost.py",
            HEAD + "class LostRouter(BaseRouter[AppContext]):\n    handlers = ()\n",
        )
        report = run_check(bot_project)
        assert any(
            "роутер LostRouter не подключён" in m for m in messages(report, "warning")
        )

    def test_base_class_of_handlers_is_not_reported(self, bot_project):
        write(
            bot_project,
            "routers/shared.py",
            HEAD + "class Base(MessageHandler[AppContext]):\n"
            "    async def handle(self): ...\n\n\n"
            "class Real(Base):\n    query = Command('real')\n\n\n"
            "class SharedRouter(BaseRouter[AppContext]):\n    handlers = (Real,)\n",
        )
        root = bot_project / "src/bot/routers/__init__.py"
        text = root.read_text(encoding="utf-8")
        root.write_text(
            text.replace(
                "# selfrot: imports",
                "from .shared import SharedRouter\n# selfrot: imports",
            ).replace(
                "# selfrot: routers", "SharedRouter,\n        # selfrot: routers"
            ),
            encoding="utf-8",
        )
        assert (
            run_check(bot_project).problems == []
        )  # Base не подключён, но от него наследуют

    def test_unreachable_after_catch_all_and_same_filter_and_double_registration(
        self, bot_project
    ):
        write(
            bot_project,
            "routers/dup.py",
            HEAD
            + "class Ban(MessageHandler[AppContext[TextMessage]]):\n    query = Command('ban')\n\n    async def handle(self): ...\n\n\n"
            "class BanAgain(MessageHandler[AppContext[TextMessage]]):\n    query = Command('ban')\n\n    async def handle(self): ...\n\n\n"
            "class Catch(MessageHandler[AppContext]):\n    async def handle(self): ...\n\n\n"
            "class After(MessageHandler[AppContext[TextMessage]]):\n    query = Text('after')\n\n    async def handle(self): ...\n\n\n"
            "class DupRouter(BaseRouter[AppContext]):\n    handlers = (Ban, BanAgain, Catch, After)\n",
        )
        root = bot_project / "src/bot/routers/__init__.py"
        text = root.read_text(encoding="utf-8")
        root.write_text(
            text.replace(
                "# selfrot: imports", "from .dup import DupRouter\n# selfrot: imports"
            ).replace("# selfrot: routers", "DupRouter,\n        # selfrot: routers"),
            encoding="utf-8",
        )
        found = messages(run_check(bot_project), "warning")
        assert any(
            "BanAgain недостижим: выше Ban тот же фильтр Command('ban')" in m
            for m in found
        )
        assert any("After недостижим: выше Catch без фильтра" in m for m in found)
        assert not any(m.startswith("Ban недостижим") for m in found)

    def test_custom_filters_with_hidden_parameters_are_not_called_identical(
        self, bot_project
    ):
        write(
            bot_project,
            "filters/owner.py",
            "from selfrot.filter import BaseFilter\n\n\n"
            "class IsUser(BaseFilter):\n"
            "    def __init__(self, user_id: int) -> None:\n        self.user_id = user_id\n\n"
            "    async def check(self, ctx) -> bool:\n        return ctx.user is not None and ctx.user.id == self.user_id\n",
        )
        write(
            bot_project,
            "routers/owners.py",
            HEAD + "from ..filters.owner import IsUser\n\n\n"
            "class One(MessageHandler[AppContext]):\n    query = IsUser(1)\n\n    async def handle(self): ...\n\n\n"
            "class Two(MessageHandler[AppContext]):\n    query = IsUser(2)\n\n    async def handle(self): ...\n\n\n"
            "class OwnersRouter(BaseRouter[AppContext]):\n    handlers = (One, Two)\n",
        )
        root = bot_project / "src/bot/routers/__init__.py"
        text = root.read_text(encoding="utf-8")
        root.write_text(
            text.replace(
                "# selfrot: imports",
                "from .owners import OwnersRouter\n# selfrot: imports",
            ).replace(
                "# selfrot: routers", "OwnersRouter,\n        # selfrot: routers"
            ),
            encoding="utf-8",
        )
        # у пользовательского фильтра repr скрывает параметр: «одинаковые» IsUser() ложным срабатыванием
        assert not any("Two недостижим" in m for m in messages(run_check(bot_project)))

    def test_no_handlers_at_all(self, bot_project):
        root = bot_project / "src/bot/routers/__init__.py"
        root.write_text(
            root.read_text(encoding="utf-8").replace("        StartRouter,\n", ""),
            encoding="utf-8",
        )
        assert any(
            "нет ни одного хендлера" in m
            for m in messages(run_check(bot_project), "warning")
        )


class TestErrors:
    def test_missing_package(self, project):
        with pytest.raises(InitError, match="selfrot init"):
            run_check(project)

    def test_bad_package_path(self, project):
        with pytest.raises(InitError):
            run_check(project, "my-bot")


def test_plural():
    assert [
        plural(n, "ошибка", "ошибки", "ошибок")
        for n in (0, 1, 2, 5, 11, 12, 21, 22, 25)
    ] == [
        "0 ошибок",
        "1 ошибка",
        "2 ошибки",
        "5 ошибок",
        "11 ошибок",
        "12 ошибок",
        "21 ошибка",
        "22 ошибки",
        "25 ошибок",
    ]


class TestCommandLine:
    def test_clean_project(self, bot_project, capsys):
        assert main(["check"]) == 0
        out = capsys.readouterr().out
        assert "Проблем не найдено." in out
        assert "хендлеров 1" in out

    def test_errors_give_exit_code_1(self, bot_project, capsys):
        write(bot_project, "filters/oops.py", "import nonexistent_thing\n")
        assert main(["check"]) == 1
        out = capsys.readouterr().out
        assert "ошибка: src.bot.filters.oops: ModuleNotFoundError" in out
        assert "Итог: 1 ошибка, 0 предупреждений." in out

    def test_warnings_pass_unless_strict(self, bot_project, capsys):
        write(
            bot_project,
            "routers/lost.py",
            HEAD + "class LostRouter(BaseRouter[AppContext]):\n    handlers = ()\n",
        )
        assert main(["check"]) == 0
        assert "предупреждение:" in capsys.readouterr().out
        assert main(["check", "--strict"]) == 1

    def test_verbose_prints_traceback(self, bot_project, capsys):
        write(bot_project, "filters/oops.py", "import nonexistent_thing\n")
        main(["check", "-v"])
        assert "Traceback" in capsys.readouterr().out

    def test_missing_package_is_a_message(self, project, capsys):
        assert main(["check"]) == 1
        assert "selfrot init" in capsys.readouterr().err

    def test_package_option(self, project, capsys):
        init_project(project, "app/bot")
        assert main(["check", "--package", "app/bot"]) == 0
        assert "Проверка app/bot" in capsys.readouterr().out

    def test_python_dash_m_selfrot_check(self, bot_project):
        env = {**os.environ, "PYTHONPATH": str(ROOT)}
        done = subprocess.run(
            [sys.executable, "-m", "selfrot", "check"],
            cwd=bot_project,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        assert done.returncode == 0, done.stderr
        assert "Проблем не найдено." in done.stdout
