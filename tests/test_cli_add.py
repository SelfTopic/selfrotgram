import importlib
from pathlib import Path

import pytest

from selfrot.cli import main
from selfrot.cli.add import (
    add_router,
    handler_class_name,
    router_class_name,
    wire_router,
)
from selfrot.cli.init import InitError, init_project

from .conftest import FakeTelegram, bind, message_update


def files(root: Path) -> set[str]:
    return {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()}


@pytest.fixture
def bot_project(project: Path) -> Path:
    init_project(project)
    return project


def root_router(root: Path) -> str:
    return (root / "src/bot/routers/__init__.py").read_text(encoding="utf-8")


async def say(dispatcher, text: str) -> None:
    await dispatcher._handle(
        dispatcher.create_context(bind(message_update(text), dispatcher.api))
    )


class TestNaming:
    @pytest.mark.parametrize(
        ("name", "router", "handler"),
        [
            ("profile", "ProfileRouter", "Profile"),
            ("user_stats", "UserStatsRouter", "UserStats"),
            ("a1", "A1Router", "A1"),
        ],
    )
    def test_class_names(self, name, router, handler):
        assert router_class_name(name) == router
        assert handler_class_name(name) == handler

    @pytest.mark.parametrize(
        "name", ["Profile", "my-router", "_x", "class", "1a", "", "a b", "профиль"]
    )
    def test_bad_names(self, bot_project, name):
        before = files(bot_project)
        with pytest.raises(InitError):
            add_router(bot_project, name)

        assert files(bot_project) == before


class TestFileRouter:
    def test_creates_one_file_and_wires_it(self, bot_project):
        before = files(bot_project)
        result = add_router(bot_project, "profile")
        assert files(bot_project) - before == {"src/bot/routers/profile.py"}
        assert result.wired and not result.manual
        text = root_router(bot_project)
        assert "from .profile import ProfileRouter" in text
        assert "        ProfileRouter,\n" in text

    def test_order_is_kept_and_markers_survive(self, bot_project):
        add_router(bot_project, "profile")
        add_router(bot_project, "admin")
        text = root_router(bot_project)
        assert (
            text.index("StartRouter,")
            < text.index("ProfileRouter,")
            < text.index("AdminRouter,")
        )
        assert "# selfrot: imports" in text
        assert "# selfrot: routers" in text

    async def test_the_new_router_answers(self, bot_project, telegram: FakeTelegram):
        add_router(bot_project, "profile")
        module = importlib.import_module("src.bot.__main__")
        dispatcher = module.Dispatcher(token="123456:TEST-token")

        await say(dispatcher, "/start")
        await say(dispatcher, "/profile")
        assert [m["text"] for m in telegram.sent] == [
            "Привет! Я бот на selfrotgram.",
            "Роутер profile подключён.",
        ]
        await dispatcher.api.close_session()

    def test_snake_case_name(self, bot_project):
        add_router(bot_project, "user_stats")
        assert (bot_project / "src/bot/routers/user_stats.py").exists()
        assert "UserStatsRouter" in root_router(bot_project)


class TestModuleRouter:
    def test_creates_only_a_folder_with_init(self, bot_project):
        before = files(bot_project)
        add_router(bot_project, "profile", module=True)
        assert files(bot_project) - before == {"src/bot/routers/profile/__init__.py"}
        assert not (bot_project / "src/bot/routers/profile.py").exists()

    def test_router_is_empty_and_ready_for_handlers(self, bot_project):
        add_router(bot_project, "profile", module=True)
        content = (bot_project / "src/bot/routers/profile/__init__.py").read_text(
            encoding="utf-8"
        )
        assert "handlers = ()" in content
        assert (
            "from ...context import AppContext" in content
        )  # на уровень глубже, чем у файла

    def test_root_router_import_is_the_same_as_for_a_file(self, bot_project, tmp_path):
        add_router(bot_project, "profile", module=True)
        assert "from .profile import ProfileRouter" in root_router(bot_project)

    async def test_handlers_can_be_added_next_to_init(
        self, bot_project, telegram: FakeTelegram
    ):
        add_router(bot_project, "profile", module=True)
        folder = bot_project / "src/bot/routers/profile"
        (folder / "commands.py").write_text(
            "from selfrot import MessageHandler\n"
            "from selfrot.filter import Command\n"
            "from selfrot.types import TextMessage\n\n"
            "from ...context import AppContext\n\n\n"
            "class Ping(MessageHandler[AppContext[TextMessage]]):\n"
            "    query = Command('ping')\n\n"
            "    async def handle(self) -> None:\n"
            "        await self.ctx.message.answer('pong')\n",
            encoding="utf-8",
        )
        init_file = folder / "__init__.py"
        text = init_file.read_text(encoding="utf-8")
        text = text.replace(
            "from ...context import AppContext\n",
            "from ...context import AppContext\nfrom .commands import Ping\n",
        )
        text = text.replace("handlers = ()", "handlers = (Ping,)")
        init_file.write_text(text, encoding="utf-8")

        module = importlib.import_module("src.bot.__main__")
        dispatcher = module.Dispatcher(token="123456:TEST-token")
        await say(dispatcher, "/ping")
        assert [m["text"] for m in telegram.sent] == ["pong"]
        await dispatcher.api.close_session()

    def test_empty_router_does_not_break_the_dispatcher(self, bot_project):
        add_router(bot_project, "profile", module=True)
        module = importlib.import_module("src.bot.__main__")
        assert module.Dispatcher(token="123456:TEST-token").used_update_types() == {
            "message"
        }


class TestSafety:
    def test_existing_router_is_an_error_and_changes_nothing(self, bot_project):
        add_router(bot_project, "profile")
        before = root_router(bot_project), files(bot_project)
        with pytest.raises(InitError, match="уже существует"):
            add_router(bot_project, "profile")

        assert (root_router(bot_project), files(bot_project)) == before

    def test_existing_folder_blocks_a_file_of_the_same_name(self, bot_project):
        add_router(bot_project, "profile", module=True)
        with pytest.raises(InitError):
            add_router(bot_project, "profile")

    def test_without_init_points_at_the_init_command(self, project):
        with pytest.raises(InitError, match="selfrot init"):
            add_router(project, "profile")

    def test_missing_markers_means_manual_wiring_and_no_edit(self, bot_project):
        path = bot_project / "src/bot/routers/__init__.py"
        path.write_text("# всё переписано вручную\nrouters = ()\n", encoding="utf-8")
        result = add_router(bot_project, "profile")
        assert not result.wired
        assert result.manual[0] == "from .profile import ProfileRouter"
        assert (
            path.read_text(encoding="utf-8")
            == "# всё переписано вручную\nrouters = ()\n"
        )
        assert (
            bot_project / "src/bot/routers/profile.py"
        ).exists()  # сам роутер создан

    def test_dry_run_changes_nothing(self, bot_project):
        before, text = files(bot_project), root_router(bot_project)
        result = add_router(bot_project, "profile", dry_run=True)
        assert result.created and result.wired
        assert files(bot_project) == before
        assert root_router(bot_project) == text

    def test_custom_package(self, project):
        init_project(project, "app/bot")
        add_router(project, "profile", "app/bot", module=True)
        assert (project / "app/bot/routers/profile/__init__.py").exists()
        assert "ProfileRouter" in (project / "app/bot/routers/__init__.py").read_text(
            encoding="utf-8"
        )


class TestWire:
    TEMPLATE = "from .a import A\n# selfrot: imports\n\nrouters = (\n    A,\n    # selfrot: routers\n)\n"

    def test_inserts_before_the_markers_keeping_indent(self):
        wired = wire_router(self.TEMPLATE, "BRouter", "b")
        assert wired == (
            "from .a import A\nfrom .b import BRouter\n# selfrot: imports\n\n"
            "routers = (\n    A,\n    BRouter,\n    # selfrot: routers\n)\n"
        )

    def test_no_markers(self):
        assert wire_router("routers = ()\n", "BRouter", "b") is None
        assert wire_router("# selfrot: imports\n", "BRouter", "b") is None  # нужны обе


class TestCommandLine:
    def test_add_router_prints_what_it_did(self, bot_project, capsys):
        assert main(["add", "router", "profile"]) == 0
        out = capsys.readouterr().out
        assert "Создано: src/bot/routers/profile.py" in out
        assert "Подключено в src/bot/routers/__init__.py: ProfileRouter" in out

    def test_module_flag_hint(self, bot_project, capsys):
        assert main(["add", "router", "profile", "--module"]) == 0
        out = capsys.readouterr().out
        assert "src/bot/routers/profile/__init__.py" in out
        assert "Хендлеры кладите модулями рядом" in out

    def test_errors_are_messages_with_exit_code_1(self, bot_project, capsys):
        main(["add", "router", "profile"])
        capsys.readouterr()
        assert main(["add", "router", "profile"]) == 1
        assert "уже существует" in capsys.readouterr().err
        assert main(["add", "router", "Bad-Name"]) == 1

    def test_manual_hint_when_markers_are_gone(self, bot_project, capsys):
        (bot_project / "src/bot/routers/__init__.py").write_text(
            "routers = ()\n", encoding="utf-8"
        )
        assert main(["add", "router", "profile"]) == 0
        out = capsys.readouterr().out
        assert "вручную" in out
        assert "from .profile import ProfileRouter" in out

    def test_dry_run(self, bot_project, capsys):
        before = files(bot_project)
        assert main(["add", "router", "profile", "--dry-run"]) == 0
        assert "Было бы создано" in capsys.readouterr().out
        assert files(bot_project) == before

    def test_package_option(self, project, capsys):
        init_project(project, "app/bot")
        assert main(["add", "router", "profile", "--package", "app/bot"]) == 0
        assert (project / "app/bot/routers/profile.py").exists()
