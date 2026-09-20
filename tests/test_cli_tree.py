import os
import subprocess
import sys
from pathlib import Path

import pytest

from selfrot import (
    BaseContext,
    BaseDispatcher,
    BaseMiddleware,
    BaseRouter,
    Bot,
    CommandArgs,
    MessageHandler,
)
from selfrot.cli import main
from selfrot.cli.add import add_router
from selfrot.cli.init import InitError, init_project
from selfrot.cli.tree import build_tree, load_dispatcher, render
from selfrot.filter import Command, FromUser, HasText, MemberJoined, Text, TextRegexp
from selfrot.handlers import CallbackQueryHandler, ChatMemberHandler
from selfrot.types import ChatMemberUpdated, TextMessage

ROOT = Path(__file__).resolve().parent.parent


class Args(CommandArgs):
    n: int


class Trace(BaseMiddleware[BaseContext]):
    async def pre_handle(self) -> bool:
        return True

    async def post_handle(self, exc=None): ...


class Ban(MessageHandler[BaseContext[TextMessage]]):
    """Забанить."""

    cmd = Command("ban", Args)
    query = FromUser(1) & cmd

    async def pre_handle(self): ...

    async def handle(self): ...

    async def on_error(self, exc):
        raise exc


class Hello(MessageHandler[BaseContext[TextMessage]]):
    query = Text("привет", ignore_case=True) | TextRegexp(r"^hi")

    async def handle(self): ...


class Anything(MessageHandler[BaseContext]):
    async def handle(self): ...


class Shadowed(MessageHandler[BaseContext[TextMessage]]):
    query = HasText()

    async def handle(self): ...


class Joined(ChatMemberHandler[BaseContext[ChatMemberUpdated]]):
    query = MemberJoined()

    async def handle(self): ...


class Press(CallbackQueryHandler[BaseContext]):
    async def handle(self): ...


class Inner(BaseRouter[BaseContext]):
    middlewares = (Trace,)
    handlers = (Ban, Hello, Anything, Shadowed, Joined)


class Empty(BaseRouter[BaseContext]):
    pass


class Root(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    middlewares = (Trace,)
    routers = (Inner, Empty)


def lines(dispatcher, **options) -> list[str]:
    return render(build_tree(dispatcher, **options)).splitlines()


@pytest.fixture
def dispatcher() -> BaseDispatcher:
    return Root(token="1:T")


class TestBuildTree:
    def test_structure_and_order(self, dispatcher):
        text = lines(dispatcher)
        assert text[0] == "Root  (мидлвари: Trace)"  # имя класса диспетчера
        inner = next(t for t in text if "Inner" in t)
        assert inner.endswith("(мидлвари: Trace)")

        tree_lines = text[1 : text.index("")]
        names = [t.lstrip("│├└─ ").split()[0] for t in tree_lines]
        # порядок проверки: хендлеры Inner, затем следующий роутер
        assert names == [
            "Inner",
            "Ban",
            "Hello",
            "Anything",
            "Shadowed",
            "Joined",
            "Empty",
        ]

    def test_handler_rows_show_kind_promise_and_filter(self, dispatcher):
        text = "\n".join(lines(dispatcher))
        assert "Ban" in text and "message: TextMessage" in text
        assert "(FromUser(1) & Command('ban', Args))" in text
        assert "(Text('привет', ignore_case=True) | TextRegexp('^hi'))" in text
        assert "chat_member: ChatMemberUpdated" in text
        assert "MemberJoined()" in text

    def test_handler_without_promise_shows_only_the_kind(self, dispatcher):
        row = next(line for line in lines(dispatcher) if "Anything" in line)
        assert "message " in row and "TextMessage" not in row

    def test_catch_all_is_named_and_shadows_later_handlers_of_its_kind(
        self, dispatcher
    ):
        text = lines(dispatcher)
        anything = next(line for line in text if "Anything" in line)
        assert "без фильтра" in anything
        shadowed = next(line for line in text if "Shadowed" in line)
        assert "недостижим: выше Anything" in shadowed
        assert "недостижим" not in next(
            line for line in text if "Joined" in line
        )  # другой вид апдейта
        assert text[-1] == "Предупреждений: 1"

    def test_totals_and_allowed_updates(self, dispatcher):
        tree = build_tree(dispatcher)
        assert (tree.routers, tree.handlers, tree.warnings) == (2, 5, 1)
        assert tree.update_types == ["chat_member", "message"]
        assert "allowed_updates: chat_member, message" in render(tree)

    def test_verbose_adds_overrides_and_docstrings(self, dispatcher):
        ban = next(line for line in lines(dispatcher, verbose=True) if "Ban" in line)
        assert "переопределено: pre_handle, on_error" in ban
        assert "Забанить." in ban
        plain = next(line for line in lines(dispatcher) if "Ban" in line)
        assert "переопределено" not in plain

    def test_ascii_mode(self, dispatcher):
        text = "\n".join(lines(dispatcher, ascii_only=True))
        assert "|-" in text and "`-" in text
        assert not any(ch in text for ch in "├└│─")

    def test_dispatcher_own_handlers_come_first(self):
        class Own(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            handlers = (Hello,)
            routers = (Inner,)

        text = lines(Own(token="1:T"))
        assert (
            text[1].strip("│├└─ ").startswith("Hello")
        )  # свои хендлеры проверяются раньше вложенных роутеров

    def test_no_handlers(self):
        class Bare(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext

        text = lines(Bare(token="1:T"))
        assert text[0] == "Bare"
        assert "allowed_updates: нет" in text[-1]

    def test_callback_handler_kind(self):
        class Buttons(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            handlers = (Press,)

        assert "callback_query" in "\n".join(lines(Buttons(token="1:T")))


class TestFilterReprs:
    def test_command(self):
        assert repr(Command("calc", Args)) == "Command('calc', Args)"
        assert (
            repr(Command("x", prefixes="/!", ignore_case=True))
            == "Command('x', prefixes='/!', ignore_case=True)"
        )
        assert repr(Command("y", args_count=2)) == "Command('y', args_count=2)"
        assert (
            repr(Command("z", Args, strict=True)) == "Command('z', Args, strict=True)"
        )
        assert repr(Command("start")) == "Command('start')"

    def test_strings(self):
        assert repr(Text("бот", ignore_case=True)) == "Text('бот', ignore_case=True)"
        assert repr(Text("бот")) == "Text('бот')"
        assert repr(TextRegexp("a", full=True)) == "TextRegexp('a', full=True)"


@pytest.fixture
def bot_project(project: Path) -> Path:
    init_project(project)
    return project


class TestCommandLine:
    def test_tree_of_a_fresh_project(self, bot_project, capsys):
        assert main(["tree"]) == 0
        out = capsys.readouterr().out.splitlines()
        assert out[0] == "Dispatcher  (мидлвари: LoggingMiddleware)"
        assert out[1] == "└─ RootRouter"
        assert out[2] == "   └─ StartRouter"
        assert out[3].split() == [
            "└─",
            "Start",
            "message:",
            "TextMessage",
            "Command('start')",
        ]
        assert (
            out[-1] == "Роутеров: 2 (без корня), хендлеров: 1. allowed_updates: message"
        )

    def test_added_routers_appear_in_order(self, bot_project, capsys):
        add_router(bot_project, "profile")
        add_router(bot_project, "shop", module=True)
        main(["tree"])
        out = capsys.readouterr().out
        assert (
            out.index("StartRouter")
            < out.index("ProfileRouter")
            < out.index("ShopRouter")
        )
        assert "Command('profile')" in out

    def test_explicit_target_and_package_option(self, project, capsys):
        init_project(project, "app/bot")
        assert main(["tree", "--package", "app/bot"]) == 0
        assert main(["tree", "app.bot.__main__:Dispatcher"]) == 0
        assert capsys.readouterr().out.count("Dispatcher") == 2

    def test_needs_no_token_and_touches_no_files(
        self, bot_project, capsys, monkeypatch
    ):
        monkeypatch.delenv("BOT_TOKEN", raising=False)
        before = {p.name for p in bot_project.iterdir()}
        assert main(["tree"]) == 0
        assert {p.name for p in bot_project.iterdir()} == before
        assert not (bot_project / "bot_cfg.cfg").exists()

    def test_missing_module_is_a_message(self, project, capsys):
        assert main(["tree"]) == 1
        assert "Не удалось импортировать src.bot.__main__" in capsys.readouterr().err

    def test_missing_class(self, bot_project, capsys):
        assert main(["tree", "src.bot.__main__:Nope"]) == 1
        assert "нет Nope" in capsys.readouterr().err

    def test_broken_project_code_shows_the_reason(self, bot_project, capsys):
        (bot_project / "src/bot/context.py").write_text(
            "raise RuntimeError('сломано')\n", encoding="utf-8"
        )
        with pytest.raises(
            RuntimeError
        ):  # ошибка импорта не ImportError: доходит как есть
            main(["tree"])

    def test_falls_back_to_plain_branches_when_the_terminal_cannot_draw_boxes(
        self, bot_project, monkeypatch
    ):
        import io

        # cp1251 (типичная консоль Windows) знает кириллицу, но не знает символы рамок
        buffer = io.TextIOWrapper(io.BytesIO(), encoding="cp1251", newline="")
        monkeypatch.setattr(sys, "stdout", buffer)
        assert main(["tree"]) == 0
        buffer.flush()
        printed = buffer.buffer.getvalue().decode("cp1251")
        assert "`- Start" in printed
        assert "мидлвари: LoggingMiddleware" in printed

    def test_python_dash_m_selfrot_tree(self, bot_project):
        env = {**os.environ, "PYTHONPATH": str(ROOT)}
        done = subprocess.run(
            [sys.executable, "-m", "selfrot", "tree", "--ascii"],
            cwd=bot_project,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        assert done.returncode == 0, done.stderr
        assert "StartRouter" in done.stdout


def test_load_dispatcher_wraps_constructor_failure(project):
    (project / "broken.py").write_text(
        "from selfrot import BaseDispatcher, Bot, BaseContext\n"
        "class Dispatcher(BaseDispatcher[BaseContext]):\n"
        "    bot = Bot\n    context = BaseContext\n"
        "    def __init__(self, token=None):\n        raise ValueError('нет подключения')\n",
        encoding="utf-8",
    )
    with pytest.raises(InitError, match="нет подключения"):
        load_dispatcher("broken", project)
    sys.modules.pop("broken", None)
