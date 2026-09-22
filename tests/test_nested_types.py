"""Условия над ответом на сообщение: Reply[...], HasReply*, пути в required_fields."""

from typing import Any

import pytest

from selfrot import BaseContext, BaseDispatcher, Bot, MessageHandler
from selfrot.cli.tree import build_tree, render
from selfrot.exceptions import DefinitionError
from selfrot import filter as filters
from selfrot import types as api_types
from selfrot.filter import (
    BaseFilter,
    Command,
    HasReplyCaption,
    HasReplyPhoto,
    HasReplyToMessage,
    HasReplyUser,
)
from selfrot.types import (
    CaptionMessage,
    Message,
    PhotoMessage,
    Reply,
    ReplyPhotoMessage,
    ReplyUserMessage,
    TextMessage,
    UserMessage,
)
from selfrot.utils.narrowing import required_fields

from .conftest import REPLY_SAMPLES, TOKEN, bind, callback_update, reply_update

SAMPLES = REPLY_SAMPLES
PHOTO = SAMPLES["photo"]["photo"]


def names(attr: str) -> tuple[str, str]:
    """user -> (HasReplyUser, ReplyUserMessage); video_note -> (HasReplyVideoNote, ...)."""
    pascal = "".join(part.capitalize() for part in attr.split("_"))
    return f"HasReply{pascal}", f"Reply{pascal}Message"


def ctx(reply: dict[str, Any] | None = None, text: str = "/x") -> BaseContext[Any]:
    """Сообщение-ответ: reply, поля того сообщения (None: не ответ)."""
    api = Bot(TOKEN)
    return BaseContext(bind(reply_update(text, reply), api), api)


class PhotoCaption(PhotoMessage, CaptionMessage, frozen=True): ...


class Warn(TextMessage, ReplyUserMessage, frozen=True): ...


class WarnPhoto(TextMessage, Reply[PhotoCaption], frozen=True): ...


class TestRequiredFields:
    def test_flat_types_are_unchanged(self):
        assert required_fields(TextMessage) == {"text"}

    def test_ready_made_alias(self):
        assert required_fields(ReplyUserMessage) == {
            "reply_to_message",
            "reply_to_message.user",
        }

    def test_conditions_of_the_reply_combine_in_the_inner_type(self):
        assert required_fields(Reply[PhotoCaption]) == {
            "reply_to_message",
            "reply_to_message.photo",
            "reply_to_message.caption",
        }

    def test_with_fields_of_the_message_itself(self):
        assert required_fields(Warn) == {
            "text",
            "reply_to_message",
            "reply_to_message.user",
        }
        assert required_fields(WarnPhoto) == {
            "text",
            "reply_to_message",
            "reply_to_message.photo",
            "reply_to_message.caption",
        }

    def test_two_levels(self):
        assert required_fields(Reply[Reply[UserMessage]]) == {
            "reply_to_message",
            "reply_to_message.reply_to_message",
            "reply_to_message.reply_to_message.user",
        }

    def test_own_nested_type_without_generics(self):
        from pydantic import ConfigDict, Field

        class RepliesToText(Message, frozen=True):
            model_config = ConfigDict(defer_build=True)
            reply_to_message: TextMessage = Field()

        assert required_fields(RepliesToText) == {
            "reply_to_message",
            "reply_to_message.text",
        }

    def test_pydantic_keeps_the_generic_argument_where_we_read_it(self):
        """Если pydantic поменяет устройство, упасть должен этот тест, а не проверка молча."""
        meta = Reply[UserMessage].__pydantic_generic_metadata__  # type: ignore[attr-defined]
        assert meta["origin"] is Reply
        assert meta["args"] == (UserMessage,)
        assert len(Reply.__pydantic_generic_metadata__["parameters"]) == 1  # type: ignore[attr-defined]


class TestFilters:
    @pytest.mark.parametrize("attr", SAMPLES)
    async def test_checks_the_field_of_the_reply(self, attr):
        filter_ = getattr(filters, names(attr)[0])()
        assert await filter_.check(ctx(SAMPLES[attr]))
        assert not await filter_.check(ctx({}))  # ответ есть, поля нет
        assert not await filter_.check(ctx(None))  # ответа нет

    @pytest.mark.parametrize("attr", SAMPLES)
    async def test_field_of_another_kind_does_not_count(self, attr):
        filter_ = getattr(filters, names(attr)[0])()
        for other, fields in SAMPLES.items():
            if other != attr:
                assert not await filter_.check(ctx(fields)), other

    @pytest.mark.parametrize("attr", SAMPLES)
    def test_guarantee_is_the_path(self, attr):
        filter_ = getattr(filters, names(attr)[0])()
        assert filter_.guarantee().fields == {
            "reply_to_message",
            f"reply_to_message.{attr}",
        }

    @pytest.mark.parametrize("attr", SAMPLES)
    def test_alias_promises_what_the_filter_checks(self, attr):
        has, alias = names(attr)
        assert required_fields(getattr(api_types, alias)) == getattr(
            filters, has
        )().guarantee().fields

    async def test_event_without_message_does_not_match(self):
        api = Bot(TOKEN)
        callback = BaseContext(bind(callback_update("x"), api), api)
        assert not await HasReplyUser().check(callback)

    def test_every_ready_made_condition_has_its_own_sample(self):
        # Не даёт списку в генераторе разойтись с тестами: новое условие = новый образец.
        # Готовое условие это алиас Reply[...]; одноимённые типы первого уровня
        # (ReplyToMessageMessage, ReplyMarkupMessage) сюда не относятся.
        ready = {
            name
            for name, value in vars(api_types).items()
            if getattr(value, "__pydantic_generic_metadata__", {}).get("origin") is Reply
        }
        assert ready == {names(attr)[1] for attr in SAMPLES}

    def test_and_unites_paths_or_intersects(self):
        both = HasReplyPhoto() & HasReplyCaption()
        either = HasReplyPhoto() | HasReplyCaption()
        assert both.guarantee().fields == {
            "reply_to_message",
            "reply_to_message.photo",
            "reply_to_message.caption",
        }
        assert either.guarantee().fields == {"reply_to_message"}

    async def test_combined_filter_needs_both(self):
        both = HasReplyPhoto() & HasReplyCaption()
        assert await both.check(ctx({"photo": PHOTO, "caption": "c"}))
        assert not await both.check(ctx({"photo": PHOTO}))
        assert not await both.check(ctx({"caption": "c"}))


class TestHandlerHeader:
    """Заголовок обещает, query проверяет: расхождение видно при импорте."""

    def test_honest_handlers_are_accepted(self):
        class One(MessageHandler[BaseContext[ReplyUserMessage]]):
            query = HasReplyUser()

            async def handle(self): ...

        class Two(MessageHandler[BaseContext[Reply[PhotoCaption]]]):
            query = HasReplyPhoto() & HasReplyCaption()

            async def handle(self): ...

        class Three(MessageHandler[BaseContext[Warn]]):
            query = Command("warn") & HasReplyUser()

            async def handle(self): ...

    def test_only_presence_of_reply_is_not_enough_for_its_user(self):
        # То, что раньше проходило молча: проверяется reply, а обещан его автор.
        with pytest.raises(DefinitionError, match="reply_to_message.user"):

            class Liar(MessageHandler[BaseContext[ReplyUserMessage]]):
                query = HasReplyToMessage()

                async def handle(self): ...

    def test_missing_second_condition(self):
        with pytest.raises(DefinitionError, match="reply_to_message.caption") as caught:

            class Half(MessageHandler[BaseContext[Reply[PhotoCaption]]]):
                query = HasReplyPhoto()

                async def handle(self): ...

        assert "reply_to_message.photo" not in str(caught.value)

    def test_or_promises_only_the_common_part(self):
        with pytest.raises(DefinitionError, match="reply_to_message.photo"):

            class Either(MessageHandler[BaseContext[ReplyPhotoMessage]]):
                query = HasReplyPhoto() | HasReplyCaption()

                async def handle(self): ...

    def test_stronger_filter_than_header_is_fine(self):
        class Weaker(MessageHandler[BaseContext[ReplyPhotoMessage]]):
            query = HasReplyPhoto() & HasReplyCaption()

            async def handle(self): ...

    def test_fields_of_the_message_itself_are_still_checked(self):
        with pytest.raises(DefinitionError, match="text"):

            class NoText(MessageHandler[BaseContext[Warn]]):
                query = HasReplyUser()

                async def handle(self): ...

    def test_own_filter_with_own_reply_type(self):
        class RepliesToAdmin(BaseFilter[BaseContext[Reply[UserMessage]]]):
            guarantees = Reply[UserMessage]

            async def check(self, ctx: BaseContext[Any]) -> bool:
                return True

        class Ok(MessageHandler[BaseContext[ReplyUserMessage]]):
            query = RepliesToAdmin()

            async def handle(self): ...


class TestTree:
    def test_header_type_is_shown_with_its_argument(self):
        class Handler(MessageHandler[BaseContext[Reply[PhotoCaption]]]):
            query = HasReplyPhoto() & HasReplyCaption()

            async def handle(self): ...

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            handlers = (Handler,)

        text = render(build_tree(Root(token="1:T")))
        assert "message: Reply[PhotoCaption]" in text
