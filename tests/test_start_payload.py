"""Deep link (t.me/<bot>?start=...): StartPayload, Command(..., deep_link=True)."""

from typing import Any

import pytest

from selfrot import (
    BaseContext,
    BaseDispatcher,
    Bot,
    CommandArgs,
    MessageHandler,
    StartPayload,
)
from selfrot.exceptions import DefinitionError, StartPayloadError
from selfrot.filter import Command
from selfrot.types import TextMessage

from .conftest import TOKEN, FakeTelegram, bind, message_update


def ctx(text: str) -> BaseContext[Any]:
    api = Bot(TOKEN)
    return BaseContext(bind(message_update(text), api), api)


class MarryLink(StartPayload, prefix="marry"):
    proposal_id: int


class TestStartPayload:
    def test_pack_and_unpack_roundtrip(self):
        link = MarryLink(proposal_id=5)
        assert link.pack() == "marry_5"
        assert MarryLink.unpack("marry_5") == link

    def test_try_unpack_wrong_prefix(self):
        assert MarryLink.try_unpack("invite_5") is None

    def test_try_unpack_wrong_type(self):
        assert MarryLink.try_unpack("marry_не_число") is None

    def test_pack_rejects_characters_outside_telegram_alphabet(self):
        class WithText(StartPayload, prefix="say"):
            text: str

        with pytest.raises(StartPayloadError, match=r"\[A-Za-z0-9_-\]"):
            WithText(text="привет").pack()

    def test_pack_rejects_too_long(self):
        class Big(StartPayload, prefix="big"):
            value: str

        with pytest.raises(StartPayloadError, match="64"):
            Big(value="x" * 70).pack()

    def test_prefix_must_be_in_telegram_alphabet(self):
        with pytest.raises(DefinitionError, match=r"\[A-Za-z0-9_-\]"):

            class Bad(StartPayload, prefix="ma ry"):
                x: int

    def test_sep_inside_prefix_is_rejected(self):
        with pytest.raises(DefinitionError, match="prefix"):

            class Bad(StartPayload, prefix="ma_ry"):
                x: int

    def test_url_needs_bot_username(self):
        bot = Bot(TOKEN)
        with pytest.raises(StartPayloadError, match="username"):
            MarryLink(proposal_id=5).url(bot)

    def test_url_builds_the_deep_link(self):
        bot = Bot(TOKEN)
        bot.username = "my_bot"
        assert MarryLink(proposal_id=5).url(bot) == "https://t.me/my_bot?start=marry_5"


class TestCommandDeepLinkValidation:
    def test_start_payload_model_without_deep_link_is_rejected(self):
        with pytest.raises(DefinitionError, match="deep_link=True"):
            Command("start", MarryLink)

    def test_command_args_model_with_deep_link_is_rejected(self):
        class Args(CommandArgs):
            x: int

        with pytest.raises(DefinitionError, match="StartPayload"):
            Command("start", Args, deep_link=True)

    def test_args_count_with_deep_link_is_rejected(self):
        with pytest.raises(DefinitionError, match="args_count"):
            Command("start", deep_link=True, args_count=1)

    def test_strict_with_deep_link_is_rejected(self):
        with pytest.raises(DefinitionError, match="strict"):
            Command("start", MarryLink, deep_link=True, strict=True)

    def test_repr_shows_deep_link(self):
        assert repr(Command("start", MarryLink, deep_link=True)) == (
            "Command('start', MarryLink, deep_link=True)"
        )


class TestBareDeepLinkCommand:
    """Command("start", deep_link=True) без модели: не своя забота — любой чужой
    deep-link токен оставляет дальше, остальное (или пусто) берёт себе."""

    def setup_method(self) -> None:
        self.start = Command("start", deep_link=True)

    async def test_matches_bare_start(self):
        assert await self.start.check(ctx("/start"))

    async def test_does_not_match_a_deep_link_shaped_token(self):
        assert not await self.start.check(ctx("/start marry_5"))
        assert not await self.start.check(ctx("/start whatever-looks_like-one"))

    async def test_matches_free_text_that_is_not_deep_link_shaped(self):
        # Несколько слов — не похоже на deep link токен (там пробелов не бывает),
        # поведение как у обычного Command: не трогаем, что не узнаём.
        assert await self.start.check(ctx("/start привет мир"))

    async def test_does_not_match_other_commands(self):
        assert not await self.start.check(ctx("/help"))


class TestTypedDeepLinkCommand:
    def setup_method(self) -> None:
        self.marry = Command("start", MarryLink, deep_link=True)

    async def test_matches_its_own_payload(self):
        assert await self.marry.check(ctx("/start marry_5"))

    async def test_parse_returns_the_typed_model(self):
        link = self.marry.parse(ctx("/start marry_5"))
        assert link == MarryLink(proposal_id=5)

    async def test_does_not_match_someone_elses_prefix(self):
        assert not await self.marry.check(ctx("/start invite_5"))

    async def test_does_not_match_bare_start(self):
        assert not await self.marry.check(ctx("/start"))

    async def test_where_filters_by_unpacked_field(self):
        class InviteLink(StartPayload, prefix="invite"):
            chat_id: int
            role: str

        cmd = Command("start", InviteLink, deep_link=True)
        admin_only = cmd.where(role="admin")
        assert await admin_only.check(ctx("/start invite_7_admin"))
        assert not await admin_only.check(ctx("/start invite_7_member"))


class TestOrderIndependence:
    """Воспроизведение запроса: без deep_link костыль с порядком — специфичный
    хендлер должен стоять раньше общего /start. С deep_link порядок не важен."""

    def dispatcher(self) -> BaseDispatcher:
        marry = Command("start", MarryLink, deep_link=True)
        start = Command("start", deep_link=True)

        class MarryByLink(MessageHandler[BaseContext[TextMessage]]):
            query = marry

            async def handle(self):
                args = marry.parse(self.ctx)
                await self.ctx.message.reply(f"Брак по ссылке: {args.proposal_id}")

        class Start(MessageHandler[BaseContext[TextMessage]]):
            query = start

            async def handle(self):
                await self.ctx.message.reply("Обычный /start")

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            # Намеренно "неправильный" порядок: общий /start выше специфичного.
            handlers = (Start, MarryByLink)

        return Root(token="1:T")

    async def feed(self, dp: BaseDispatcher, text: str) -> None:
        await dp._handle(dp.create_context(bind(message_update(text), dp.api)))

    async def test_deep_link_reaches_its_handler_despite_the_order(
        self, telegram: FakeTelegram
    ):
        dp = self.dispatcher()
        await self.feed(dp, "/start marry_5")
        assert telegram.sent[-1]["text"] == "Брак по ссылке: 5"
        await dp.api.close_session()

    async def test_bare_start_still_works(self, telegram: FakeTelegram):
        dp = self.dispatcher()
        await self.feed(dp, "/start")
        assert telegram.sent[-1]["text"] == "Обычный /start"
        await dp.api.close_session()

    async def test_unknown_deep_link_shaped_token_falls_through_to_nothing(
        self, telegram: FakeTelegram
    ):
        dp = self.dispatcher()
        await self.feed(dp, "/start invite_abc")
        assert telegram.sent == []
        await dp.api.close_session()
