from typing import Any

import pytest

from selfrot import BaseContext, BaseDispatcher, Bot, CommandArgs, MessageHandler
from selfrot.exceptions import CommandArgsError, DefinitionError, FilterMatchError
from selfrot.filter import AnyCommand, Command, FromUser, HasText
from selfrot.types import PhotoMessage, TextMessage

from .conftest import TOKEN, FakeTelegram, bind, message_update


def ctx(text: str, uid: int = 7) -> BaseContext[Any]:
    api = Bot(TOKEN)
    return BaseContext(bind(message_update(text, uid=uid), api), api)


class TransferArgs(CommandArgs):
    to: str
    amount: int


class TopUpArgs(CommandArgs):
    amount: int


def transfer() -> AnyCommand[TransferArgs]:
    return AnyCommand(
        Command("transfer", TransferArgs, ignore_case=True),
        Command("перевести", TransferArgs, prefixes="", ignore_case=True),
        Command("кинуть", TransferArgs, prefixes="", ignore_case=True),
    )


class TestFilter:
    @pytest.mark.parametrize(
        "text",
        ["/transfer @a 100", "/TRANSFER @a 100", "перевести @a 100", "Кинуть @a 100"],
    )
    async def test_any_trigger_matches(self, text: str):
        assert await transfer().check(ctx(text))

    @pytest.mark.parametrize(
        "text",
        [
            "привет",
            "/перевести @a 100",  # у «перевести» префикса нет
            "transfer @a 100",  # а у transfer префикс обязателен
            "/transferx @a 100",
        ],
    )
    async def test_nothing_else_matches(self, text: str):
        assert not await transfer().check(ctx(text))

    async def test_message_without_text(self):
        api = Bot(TOKEN)
        c = BaseContext(bind(message_update(None), api), api)
        assert not await transfer().check(c)

    async def test_strict_belongs_to_each_command(self):
        group = AnyCommand(
            Command("a", TopUpArgs, strict=True),
            Command("b", TopUpArgs),
        )
        assert not await group.check(ctx("/a x"))
        assert await group.check(ctx("/a 5"))
        assert await group.check(ctx("/b x"))  # не strict: подходит, parse даст ошибку


class TestParse:
    def test_parses_with_the_trigger_that_matched(self):
        group = transfer()
        expected = TransferArgs(to="@a", amount=100)
        assert group.parse(ctx("/transfer @a 100")) == expected
        assert group.parse(ctx("перевести @a 100")) == expected
        assert group.parse(ctx("КИНУТЬ @a 100")) == expected

    def test_find_tells_which_one(self):
        group = transfer()
        assert group.find(ctx("кинуть @a 1")).name == "кинуть"
        assert group.find(ctx("/transfer @a 1")).name == "transfer"

    def test_first_of_the_list_wins(self):
        first = Command("go", TopUpArgs)
        second = Command("go", TopUpArgs, ignore_case=True)
        assert AnyCommand(first, second).find(ctx("/go 1")) is first
        assert AnyCommand(second, first).find(ctx("/go 1")) is second

    def test_bad_args_carry_usage_of_the_trigger_written(self):
        group = transfer()
        with pytest.raises(CommandArgsError) as caught:
            group.parse(ctx("перевести @a"))

        assert caught.value.usage == "перевести <to> <amount>"

        with pytest.raises(CommandArgsError) as caught:
            group.parse(ctx("/transfer @a много"))

        assert caught.value.usage == "/transfer <to> <amount>"

    def test_parse_and_find_without_a_match_raise(self):
        with pytest.raises(FilterMatchError):
            transfer().parse(ctx("привет"))
        with pytest.raises(FilterMatchError):
            transfer().find(ctx("привет"))

    def test_different_models_per_trigger(self):
        group = AnyCommand(
            Command("transfer", TransferArgs),
            Command("пополнить", TopUpArgs, prefixes=""),
        )
        first = group.parse(ctx("/transfer @a 5"))
        second = group.parse(ctx("пополнить 9"))

        assert first == TransferArgs(to="@a", amount=5)
        assert second == TopUpArgs(amount=9)

        match second:
            case TransferArgs():
                pytest.fail("ожидалась TopUpArgs")
            case TopUpArgs(amount=amount):
                assert amount == 9

    def test_commands_without_a_model_give_raw_call(self):
        group = AnyCommand(Command("x"), Command("икс", prefixes=""))
        call = group.parse(ctx("икс а б"))
        assert call.prefix == "" and call.args == ("а", "б")


class TestDefinition:
    def test_needs_at_least_one_command(self):
        with pytest.raises(DefinitionError, match="хотя бы одна"):
            AnyCommand()

    def test_matches_is_check_without_await(self):
        cmd = Command("go", TopUpArgs, strict=True)
        assert cmd.matches(ctx("/go 1"))
        assert not cmd.matches(ctx("/go x"))
        assert not cmd.matches(ctx("привет"))

    def test_repr_lists_every_trigger(self):
        assert repr(transfer()) == (
            "AnyCommand("
            "Command('transfer', TransferArgs, ignore_case=True), "
            "Command('перевести', TransferArgs, prefixes='', ignore_case=True), "
            "Command('кинуть', TransferArgs, prefixes='', ignore_case=True))"
        )

    def test_guarantees_text_like_command(self):
        class Ok(MessageHandler[BaseContext[TextMessage]]):
            query = transfer()

            async def handle(self): ...

        with pytest.raises(DefinitionError):

            class Bad(MessageHandler[BaseContext[PhotoMessage]]):
                query = transfer()

                async def handle(self): ...

    def test_combines_with_other_filters(self):
        class Ok(MessageHandler[BaseContext[TextMessage]]):
            query = FromUser(7) & transfer()

            async def handle(self): ...

        assert Ok.query.guarantee().fields >= HasText().guarantee().fields  # type: ignore[union-attr]

    async def test_plain_or_still_works_as_a_filter(self):
        either = Command("a") | Command("b")
        assert await either.check(ctx("/a"))
        assert await either.check(ctx("/b"))
        assert not await either.check(ctx("/c"))


TRANSFER = transfer()


class Transfer(MessageHandler[BaseContext[TextMessage]]):
    query = TRANSFER

    async def handle(self):
        args = TRANSFER.parse(self.ctx)
        await self.ctx.message.answer(f"{args.to}: {args.amount}")

    async def on_error(self, exc: Exception):
        if isinstance(exc, CommandArgsError):
            await self.ctx.message.answer(f"Пишите: {exc.usage}")
            return
        raise exc


class Root(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Transfer,)


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

    async def test_every_trigger_reaches_the_same_handler(self, say):
        assert await say("/transfer @a 100") == ["@a: 100"]
        assert await say("перевести @a 100") == ["@a: 100"]
        assert await say("кинуть @a 5") == ["@a: 5"]
        assert await say("привет") == []

    async def test_error_answers_with_the_written_trigger(self, say):
        assert await say("кинуть @a") == ["Пишите: кинуть <to> <amount>"]
        assert await say("/transfer @a x") == ["Пишите: /transfer <to> <amount>"]
