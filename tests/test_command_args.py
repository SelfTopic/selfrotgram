from enum import Enum
from typing import Literal

import pytest

from selfrot import BaseContext, BaseDispatcher, Bot, CommandArgs, MessageHandler, Rest
from selfrot.exceptions import CommandArgsError, DefinitionError, FilterMatchError
from selfrot.filter import Command
from selfrot.filter.command import CommandCall
from selfrot.types import TextMessage

from .conftest import TOKEN, FakeTelegram, bind, message_update


def ctx(text: str) -> BaseContext:
    api = Bot(TOKEN)
    return BaseContext(bind(message_update(text), api), api)


class CalcArgs(CommandArgs):
    one: int
    operator: Literal["+", "-", "*", "/"]
    two: int


class Color(Enum):
    RED = "r"
    BLUE = "b"


class RemindArgs(CommandArgs):
    minutes: int
    color: Color = Color.RED
    loud: bool = False


class SayArgs(CommandArgs):
    times: int = 1
    text: Rest = ""


class TestParse:
    async def test_types_are_converted(self):
        cmd = Command("calc", CalcArgs)
        context = ctx("/calc 12 * 3")
        assert await cmd.check(context)
        args = cmd.parse(context)
        assert isinstance(args, CalcArgs)
        assert (args.one, args.operator, args.two) == (12, "*", 3)

    async def test_optional_trailing_arguments_take_defaults(self):
        cmd = Command("remind", RemindArgs)
        assert cmd.parse(ctx("/remind 5")) == RemindArgs(
            minutes=5, color=Color.RED, loud=False
        )
        assert cmd.parse(ctx("/remind 5 b 1")) == RemindArgs(
            minutes=5, color=Color.BLUE, loud=True
        )

    async def test_rest_takes_the_tail_with_spaces_kept(self):
        cmd = Command("say", SayArgs)
        assert cmd.parse(ctx("/say 3 привет   как  дела ")) == SayArgs(
            times=3, text="привет   как  дела"
        )
        assert cmd.parse(ctx("/say")) == SayArgs(times=1, text="")

    async def test_rest_only_command_without_prefix(self):
        class Tell(CommandArgs):
            text: Rest

        cmd = Command("бот скажи", Tell, prefixes="", ignore_case=True)
        assert cmd.parse(ctx("Бот  Скажи   привет  мир")).text == "привет  мир"

    async def test_call_is_available_for_both_variants(self):
        assert Command("calc", CalcArgs).call(ctx("/calc 1 + 2")).args == (
            "1",
            "+",
            "2",
        )
        plain = Command("echo")
        assert isinstance(plain.parse(ctx("/echo привет")), CommandCall)
        assert plain.parse(ctx("/echo привет")).rest == "привет"

    async def test_prefixes_and_mention_still_work(self):
        cmd = Command("calc", CalcArgs, prefixes="/!")
        assert cmd.parse(ctx("!calc 1 + 1")).two == 1
        api = Bot(TOKEN)
        api.username = "test_bot"
        mention = BaseContext(bind(message_update("/calc@Test_Bot 1 + 1"), api), api)
        assert cmd.parse(mention).one == 1

    async def test_matches_by_name_only_so_wrong_arguments_reach_parse(self):
        cmd = Command("calc", CalcArgs)
        assert await cmd.check(ctx("/calc"))
        assert await cmd.check(ctx("/calc x y z"))
        assert not await cmd.check(ctx("/other 1 + 1"))
        assert not await cmd.check(ctx("calc 1 + 1"))


class TestCommandArgsError:
    @pytest.mark.parametrize(
        ("text", "field", "fragment"),
        [
            ("/calc 1 + x", "two", "целое число"),
            ("/calc 1 ^ 2", "operator", "недопустимое значение"),
            ("/calc 1 +", "two", "не хватает"),
            ("/calc", "one", "не хватает"),
        ],
    )
    def test_problems_name_the_field(self, text, field, fragment):
        cmd = Command("calc", CalcArgs)
        with pytest.raises(CommandArgsError) as info:
            cmd.parse(ctx(text))

        problems = {p.field: p.message for p in info.value.problems}
        assert fragment in problems[field]

    def test_too_many_arguments(self):
        with pytest.raises(CommandArgsError) as info:
            Command("calc", CalcArgs).parse(ctx("/calc 1 + 2 3 4"))

        assert any("лишние аргументы: 3 4" in p.message for p in info.value.problems)

    def test_error_carries_usage_command_and_text(self):
        with pytest.raises(CommandArgsError) as info:
            Command("calc", CalcArgs).parse(ctx("/calc 1 + x"))

        error = info.value
        assert error.usage == "/calc <one> <operator: +|-|*|/> <two>"
        assert error.command == "calc"
        assert error.text == "1 + x"
        assert "/calc <one>" in str(error)
        assert isinstance(error, ValueError)

    def test_usage_marks_optional_and_rest(self):
        assert Command("remind", RemindArgs).usage == "/remind <minutes> [color] [loud]"
        assert Command("say", SayArgs).usage == "/say [times] [text...]"
        assert Command("echo").usage == "/echo"

    def test_bool_error_is_readable(self):
        with pytest.raises(CommandArgsError) as info:
            Command("remind", RemindArgs).parse(ctx("/remind 5 r maybe"))

        assert "да/нет" in info.value.problems[0].message


class TestStrictMode:
    async def test_bad_arguments_mean_no_match(self):
        cmd = Command("calc", CalcArgs, strict=True)
        assert await cmd.check(ctx("/calc 1 + 2"))
        assert not await cmd.check(ctx("/calc 1 + x"))
        assert not await cmd.check(ctx("/calc"))


class TestDefinition:
    def test_required_after_optional(self):
        with pytest.raises(DefinitionError, match="после необязательного"):

            class Bad(CommandArgs):
                a: int = 1
                b: int

    def test_rest_must_be_last(self):
        with pytest.raises(DefinitionError, match="последним"):

            class Bad(CommandArgs):
                text: Rest
                n: int = 1

    def test_model_and_args_count_conflict(self):
        with pytest.raises(DefinitionError):
            Command("calc", CalcArgs, args_count=3)  # type: ignore[call-overload]

    async def test_legacy_args_count_is_unchanged(self):
        cmd = Command("sum", args_count=2)
        assert await cmd.check(ctx("/sum 1 2"))
        assert not await cmd.check(ctx("/sum 1"))

    async def test_parse_without_check_raises(self):
        with pytest.raises(FilterMatchError):
            Command("calc", CalcArgs).parse(ctx("привет"))


class Calc(MessageHandler[BaseContext[TextMessage]]):
    cmd = Command("calc", CalcArgs)
    query = cmd

    async def pre_handle(self):
        self.args = self.cmd.parse(self.ctx)

    async def handle(self):
        a = self.args
        result = {
            "+": a.one + a.two,
            "-": a.one - a.two,
            "*": a.one * a.two,
            "/": a.one / a.two,
        }[a.operator]
        await self.ctx.message.answer(f"{a.one} {a.operator} {a.two} = {result}")

    async def on_error(self, exc: Exception):
        if isinstance(exc, CommandArgsError):
            await self.ctx.message.answer(f"Не так. Пишите: {exc.usage}")
            return
        raise exc


class Root(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Calc,)


class TestEndToEnd:
    @pytest.fixture
    async def say(self, telegram: FakeTelegram):
        dp = Root(token=TOKEN)

        async def send(text: str) -> list[str]:
            telegram.clear()
            await dp._handle(dp.create_context(bind(message_update(text), dp.api)))
            return [body["text"] for body in telegram.sent]

        yield send
        await dp.api.close_session()

    async def test_valid_and_invalid(self, say):
        assert await say("/calc 2 + 3") == ["2 + 3 = 5"]
        assert await say("/calc 6 / 3") == ["6 / 3 = 2.0"]
        assert await say("/calc 2 + x") == [
            "Не так. Пишите: /calc <one> <operator: +|-|*|/> <two>"
        ]
        assert await say("/calc") == [
            "Не так. Пишите: /calc <one> <operator: +|-|*|/> <two>"
        ]
        assert await say("привет") == []
