import pytest
from pydantic import TypeAdapter

from selfrot import BaseContext, Bot
from selfrot.exceptions import BotNotBoundError
from selfrot.types import (
    ChatMember,
    ChatMemberMember,
    InaccessibleMessage,
    InlineQueryResultArticle,
    InputMediaPhoto,
    InputTextMessageContent,
    Message,
    MessageOrigin,
    MessageOriginUser,
    ReactionType,
    ReactionTypeEmoji,
    RichText,
    RichTextBold,
    TextMessage,
    Update,
    User,
)

from .conftest import (
    FakeTelegram,
    bind,
    callback_update,
    message_result,
    message_update,
)

U = {"id": 7, "is_bot": False, "first_name": "u"}


class TestTypeParsing:
    def test_accessible_and_inaccessible_messages_are_told_apart(self):
        def parse(date: int):
            raw = callback_update("d")
            raw["callback_query"]["message"] = {
                "message_id": 1,
                "date": date,
                "chat": {"id": 5, "type": "private"},
            }
            return TypeAdapter(Update).validate_python(raw).callback_query.message

        assert type(parse(1700000000)) is Message
        inaccessible = parse(0)
        assert isinstance(inaccessible, InaccessibleMessage)
        assert not isinstance(inaccessible, Message)

    def test_discriminated_unions(self):
        assert isinstance(
            TypeAdapter(ReactionType).validate_python({"type": "emoji", "emoji": "👍"}),
            ReactionTypeEmoji,
        )
        assert isinstance(
            TypeAdapter(MessageOrigin).validate_python(
                {"type": "user", "date": 0, "sender_user": U}
            ),
            MessageOriginUser,
        )
        assert isinstance(
            TypeAdapter(ChatMember).validate_python({"status": "member", "user": U}),
            ChatMemberMember,
        )

    def test_recursive_rich_text(self):
        parsed = TypeAdapter(RichText).validate_python(
            {"type": "bold", "text": {"type": "italic", "text": "x"}}
        )
        assert isinstance(parsed, RichTextBold)

    def test_single_valued_type_fields_have_defaults(self):
        assert InputMediaPhoto(media="id").type == "photo"
        article = InlineQueryResultArticle(
            id="1",
            title="t",
            input_message_content=InputTextMessageContent(message_text="hi"),
        )
        assert article.type == "article"
        assert RichTextBold(text="x").type == "bold"
        assert (
            ChatMemberMember(user=User(id=1, is_bot=False, first_name="u")).status
            == "member"
        )

    def test_from_is_user(self):
        message = bind(message_update("x", uid=42), None).message
        assert message.user.id == 42


class TestBoundMethods:
    @pytest.fixture
    def message(self, telegram: FakeTelegram, bot: Bot) -> Message:
        raw = message_update("x", chat=-5) | {}
        raw["message"] |= {
            "message_thread_id": 9,
            "is_topic_message": True,
            "business_connection_id": "bc",
            "message_id": 42,
        }
        return bind(raw, bot).message

    async def test_answer_carries_business_and_topic(self, telegram, message):
        await message.answer("a")
        assert telegram.sent[-1] == {
            "chat_id": -5,
            "text": "a",
            "business_connection_id": "bc",
            "message_thread_id": 9,
        }

    async def test_explicit_thread_wins(self, telegram, message):
        await message.answer("a", message_thread_id=1)
        assert telegram.sent[-1]["message_thread_id"] == 1

    async def test_reply_quotes_the_message(self, telegram, message):
        await message.reply("r")
        assert telegram.sent[-1]["reply_parameters"] == {"message_id": 42}

    async def test_answer_photo(self, telegram, message):
        await message.answer_photo("file_id", caption="c")
        assert telegram.last()[0] == "sendPhoto"

    @pytest.mark.parametrize(
        ("call", "method", "expected"),
        [
            (lambda m: m.pin(), "pinChatMessage", {"chat_id": -5, "message_id": 42}),
            (lambda m: m.delete(), "deleteMessage", {"chat_id": -5, "message_id": 42}),
            (
                lambda m: m.forward(chat_id=77),
                "forwardMessage",
                {"chat_id": 77, "from_chat_id": -5, "message_id": 42},
            ),
            (
                lambda m: m.copy_to(chat_id=77),
                "copyMessage",
                {"chat_id": 77, "from_chat_id": -5, "message_id": 42},
            ),
            (
                lambda m: m.edit_reply_markup(),
                "editMessageReplyMarkup",
                {"chat_id": -5, "message_id": 42},
            ),
        ],
    )
    async def test_object_methods_target_this_message(
        self, telegram, message, call, method, expected
    ):
        await call(message)
        assert telegram.last() == (method, expected)

    async def test_edit_text_takes_text_positionally(self, telegram, message):
        await message.edit_text("новый")
        assert telegram.last() == (
            "editMessageText",
            {"chat_id": -5, "message_id": 42, "text": "новый"},
        )

    async def test_sent_message_can_edit_and_delete_itself(self, telegram, bot):
        incoming = bind(message_update("нарезка", chat=5), bot).message
        processing = await incoming.reply("⏳")
        await processing.edit_text("почти готово")
        await processing.delete()
        assert telegram.methods() == ["sendMessage", "editMessageText", "deleteMessage"]
        assert telegram.calls[1][1]["message_id"] == processing.message_id

    async def test_callback_and_inline_answers(self, telegram, bot):
        callback = bind(callback_update("go"), bot).callback_query
        await callback.answer("готово", show_alert=True)
        assert telegram.last() == (
            "answerCallbackQuery",
            {"callback_query_id": "cq1", "text": "готово", "show_alert": True},
        )

        raw = {
            "update_id": 1,
            "inline_query": {"id": "iq1", "from": U, "query": "q", "offset": ""},
        }
        await bind(raw, bot).inline_query.answer(results=[])
        assert telegram.last()[1]["inline_query_id"] == "iq1"

    async def test_nested_messages_are_bound_too(self, telegram, bot):
        raw = message_update("x")
        raw["message"]["reply_to_message"] = message_result("цитата")
        await bind(raw, bot).message.reply_to_message.answer("на цитату")
        assert telegram.sent[-1]["text"] == "на цитату"

    async def test_narrowed_types_inherit_methods(self):
        assert hasattr(TextMessage, "answer")
        assert hasattr(TextMessage, "edit_text")

    async def test_result_of_bot_call_is_bound(self, telegram, bot):
        sent = await bot.send_message(5, "x")
        await sent.delete()
        assert telegram.last() == (
            "deleteMessage",
            {"chat_id": 1, "message_id": sent.message_id},
        )

    async def test_unbound_object_explains_itself(self):
        unbound = Update(update_id=1, message=message_result())
        with pytest.raises(BotNotBoundError, match="не привязан"):
            await unbound.message.answer("x")


class TestContextShortcuts:
    @pytest.fixture
    def ctx(self, bot: Bot) -> BaseContext:
        return BaseContext(bind(message_update("x", chat=5), bot), bot)

    async def test_edit_with_only_message_id_takes_chat_from_update(
        self, telegram, ctx
    ):
        await ctx.edit_message_text("a", message_id=9)
        assert telegram.last() == (
            "editMessageText",
            {"chat_id": 5, "message_id": 9, "text": "a"},
        )

    async def test_edit_update_message_and_explicit_and_inline(self, telegram, ctx):
        await ctx.edit_message_text("b")
        assert telegram.last()[1] == {"chat_id": 5, "message_id": 1, "text": "b"}
        await ctx.edit_message_text("c", chat_id=77, message_id=3)
        assert telegram.last()[1] == {"chat_id": 77, "message_id": 3, "text": "c"}
        await ctx.edit_message_text("d", inline_message_id="inl")
        assert telegram.last()[1] == {"inline_message_id": "inl", "text": "d"}

    async def test_callback_from_inaccessible_message_still_addressable(
        self, telegram, bot
    ):
        raw = callback_update("x")
        raw["callback_query"]["message"] = {
            "message_id": 44,
            "date": 0,
            "chat": {"id": 5, "type": "private"},
        }
        ctx = BaseContext(bind(raw, bot), bot)
        await ctx.edit_message_text("готово")
        assert telegram.last()[1] == {"chat_id": 5, "message_id": 44, "text": "готово"}

    async def test_answer_and_reply_shortcuts(self, telegram, ctx):
        await ctx.answer_message("a")
        assert telegram.sent[-1] == {"chat_id": 5, "text": "a"}
        await ctx.reply_message("r")
        assert telegram.sent[-1]["reply_parameters"] == {"message_id": 1}
