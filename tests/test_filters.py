import pytest

from selfrot import BaseContext, Bot, MessageHandler
from selfrot.exceptions import DefinitionError, FilterMatchError
from selfrot.filter import (
    CallbackData,
    CallbackDataContains,
    CallbackDataEndswith,
    CallbackDataRegexp,
    CallbackDataStartswith,
    Command,
    FromUser,
    HasCaption,
    HasDataCallbackQuery,
    HasPhoto,
    HasText,
    Text,
    TextContains,
    TextEndswith,
    TextRegexp,
    TextStartswith,
)
from selfrot.types import PhotoMessage, TextMessage

from .conftest import TOKEN, bind, callback_update, message_update

PHOTO = [{"file_id": "a", "file_unique_id": "b", "width": 1, "height": 1}]


def ctx(raw: dict, username: str | None = None) -> BaseContext:
    api = Bot(TOKEN)
    api.username = username
    return BaseContext(bind(raw, api), api)


def text(value: str, **kw) -> BaseContext:
    return ctx(message_update(value, **kw))


class TestTextFilters:
    @pytest.mark.parametrize(
        ("flt", "value", "expected"),
        [
            (Text("бот"), "бот", True),
            (Text("бот"), "Бот", False),  # регистр по умолчанию учитывается
            (Text("бот", ignore_case=True), "БОТ", True),
            (Text("бот"), "бот!", False),
            (TextStartswith("мут"), "мут вася", True),
            (TextStartswith("мут"), "не мут", False),
            (TextEndswith("!"), "привет!", True),
            (TextContains("ку"), "приКУсить", False),
            (TextContains("ку", ignore_case=True), "приКУсить", True),
        ],
    )
    async def test_text_family(self, flt, value, expected):
        assert await flt.check(text(value)) is expected

    async def test_photo_without_text_does_not_match(self):
        assert not await Text("x").check(ctx(message_update(None, photo=PHOTO)))

    async def test_regexp_and_match(self):
        pattern = TextRegexp(r"(\w+) мут (\d+)")
        context = text("вася мут 15")
        assert await pattern.check(context)
        assert pattern.match(context).groups() == ("вася", "15")

    async def test_regexp_full(self):
        assert not await TextRegexp(r"\d+", full=True).check(text("12 abc"))
        assert await TextRegexp(r"\d+", full=True).check(text("12"))

    async def test_match_without_check_raises(self):
        with pytest.raises(FilterMatchError):
            TextRegexp("xyz").match(text("привет"))


class TestCommand:
    async def test_prefixes_and_args(self):
        cmd = Command("imut", args_count=1, prefixes="/!")
        assert await cmd.check(text("/imut 5"))
        assert await cmd.check(text("!imut 5"))
        assert not await cmd.check(text("/imut"))
        assert not await cmd.check(text("/imut 1 2"))
        assert not await cmd.check(text("?imut 5"))

    async def test_parse(self):
        cmd = Command("бот скажи", prefixes="", ignore_case=True)
        context = text("Бот  Скажи   привет   мир ")
        assert await cmd.check(context)
        call = cmd.parse(context)
        assert call.rest == "привет   мир"
        assert call.args == ("привет", "мир")

    async def test_multiword_needs_all_words(self):
        assert not await Command("бот скажи", prefixes="").check(text("бот"))
        assert not await Command("бот скажи", prefixes="").check(text("ботскажи x"))

    async def test_mention_only_for_this_bot(self):
        cmd = Command("start")
        assert await cmd.check(
            ctx(message_update("/start@Test_Bot"), username="test_bot")
        )
        assert not await cmd.check(
            ctx(message_update("/start@other_bot"), username="test_bot")
        )
        assert not await cmd.check(
            ctx(message_update("/start@test_bot"), username=None)
        )

    @pytest.mark.parametrize("name", ["", "/x"])
    def test_bad_name_is_definition_error(self, name):
        with pytest.raises(DefinitionError):
            Command(name)


class TestCallbackDataFilters:
    @pytest.mark.parametrize(
        ("flt", "data", "expected"),
        [
            (CallbackData("imut"), "imut", True),
            (CallbackData("imut"), "imut2", False),
            (CallbackDataStartswith("mut:"), "mut:5", True),
            (CallbackDataEndswith(":ok"), "a:ok", True),
            (CallbackDataContains("-"), "a-b", True),
            (CallbackDataRegexp(r"duel:(\d+)", full=True), "duel:42", True),
            (CallbackDataRegexp(r"duel:(\d+)", full=True), "duel:42x", False),
        ],
    )
    async def test_family(self, flt, data, expected):
        assert await flt.check(ctx(callback_update(data))) is expected

    async def test_message_is_not_callback(self):
        assert not await CallbackData("x").check(text("x"))

    async def test_callback_without_data(self):
        assert not await CallbackData("x").check(ctx(callback_update(None)))


class TestFromUser:
    async def test_message_and_callback(self):
        admins = FromUser(1, 2)
        assert await admins.check(text("x", uid=1))
        assert await admins.check(ctx(callback_update("d", uid=2)))
        assert not await admins.check(text("x", uid=3))

    async def test_event_without_user(self):
        post = {
            "update_id": 1,
            "channel_post": {
                "message_id": 1,
                "date": 5,
                "chat": {"id": -1, "type": "channel", "title": "c"},
                "text": "x",
            },
        }
        assert not await FromUser(1).check(ctx(post))

    async def test_empty_matches_nobody(self):
        assert not await FromUser().check(text("x"))


class TestCombinators:
    async def test_and_or_not_truth_table(self):
        yes, no = Text("да"), Text("нет")
        context = text("да")
        assert await (yes & yes).check(context)
        assert not await (yes & no).check(context)
        assert await (no | yes).check(context)
        assert not await (no | no).check(context)
        assert await (~no).check(context)
        assert not await (~yes).check(context)

    async def test_short_circuit(self):
        calls: list[str] = []

        class Spy(Text):
            async def check(self, ctx):  # type: ignore[override]
                calls.append("spy")
                return True

        context = text("x")
        await (Text("нет") & Spy("x")).check(context)
        await (Text("x") | Spy("x")).check(context)
        assert calls == []

    async def test_photo_and_caption(self):
        both = HasPhoto() & HasCaption()
        assert await both.check(ctx(message_update(None, photo=PHOTO, caption="кот")))
        assert not await both.check(ctx(message_update(None, photo=PHOTO)))

    def test_guarantee_arithmetic(self):
        assert (HasPhoto() & HasCaption()).guarantee().fields == {"photo", "caption"}
        assert (HasText() | HasCaption()).guarantee().fields == frozenset()
        assert (~HasText()).guarantee().fields == frozenset()
        assert (Command("a") | Command("b")).guarantee().fields == {"text"}

    def test_mixed_roots_rejected(self):
        with pytest.raises(DefinitionError):
            HasText() & HasDataCallbackQuery()


class TestHandlerHeaderCheck:
    def test_header_needs_matching_guarantee(self):
        with pytest.raises(DefinitionError, match="text"):

            class NoGuarantee(MessageHandler[BaseContext[TextMessage]]):
                query = None

                async def handle(self): ...

    def test_union_of_guarantees_satisfies_header(self):
        class Photo(PhotoMessage, frozen=True):
            pass

        class Ok(MessageHandler[BaseContext[TextMessage]]):
            query = HasText() & FromUser(1)

            async def handle(self): ...

    def test_or_loses_guarantees(self):
        with pytest.raises(DefinitionError):

            class Bad(MessageHandler[BaseContext[TextMessage]]):
                query = HasText() | FromUser(1)

                async def handle(self): ...

    def test_wrong_kind_rejected(self):
        from selfrot.filter import MemberJoined

        with pytest.raises(DefinitionError):

            class Bad(MessageHandler[BaseContext[TextMessage]]):
                query = MemberJoined()

                async def handle(self): ...
