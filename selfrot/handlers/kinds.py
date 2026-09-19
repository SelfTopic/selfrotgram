# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram Bot API 10.3, August 24, 2026.
# Руками не править — обновилась спека, перегенерировать.
# ruff: noqa
from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel

from ..context import TContext
from ..types import (
    Message,
    BusinessConnection,
    BusinessMessagesDeleted,
    MessageReactionUpdated,
    MessageReactionCountUpdated,
    InlineQuery,
    ChosenInlineResult,
    CallbackQuery,
    ShippingQuery,
    PreCheckoutQuery,
    PaidMediaPurchased,
    Poll,
    PollAnswer,
    ChatMemberUpdated,
    ChatJoinRequest,
    ChatBoostUpdated,
    ChatBoostRemoved,
    ManagedBotUpdated,
    BotSubscriptionUpdated,
    MessageGenerationStopped,
)
from .base import BaseHandler


class MessageHandler(BaseHandler[TContext]):
    """Апдейты с полем `message` (Message)."""

    update_field: ClassVar[str] = "message"
    payload_type: ClassVar[type[BaseModel]] = Message


class EditedMessageHandler(BaseHandler[TContext]):
    """Апдейты с полем `edited_message` (Message)."""

    update_field: ClassVar[str] = "edited_message"
    payload_type: ClassVar[type[BaseModel]] = Message


class ChannelPostHandler(BaseHandler[TContext]):
    """Апдейты с полем `channel_post` (Message)."""

    update_field: ClassVar[str] = "channel_post"
    payload_type: ClassVar[type[BaseModel]] = Message


class EditedChannelPostHandler(BaseHandler[TContext]):
    """Апдейты с полем `edited_channel_post` (Message)."""

    update_field: ClassVar[str] = "edited_channel_post"
    payload_type: ClassVar[type[BaseModel]] = Message


class BusinessConnectionHandler(BaseHandler[TContext]):
    """Апдейты с полем `business_connection` (BusinessConnection)."""

    update_field: ClassVar[str] = "business_connection"
    payload_type: ClassVar[type[BaseModel]] = BusinessConnection


class BusinessMessageHandler(BaseHandler[TContext]):
    """Апдейты с полем `business_message` (Message)."""

    update_field: ClassVar[str] = "business_message"
    payload_type: ClassVar[type[BaseModel]] = Message


class EditedBusinessMessageHandler(BaseHandler[TContext]):
    """Апдейты с полем `edited_business_message` (Message)."""

    update_field: ClassVar[str] = "edited_business_message"
    payload_type: ClassVar[type[BaseModel]] = Message


class DeletedBusinessMessagesHandler(BaseHandler[TContext]):
    """Апдейты с полем `deleted_business_messages` (BusinessMessagesDeleted)."""

    update_field: ClassVar[str] = "deleted_business_messages"
    payload_type: ClassVar[type[BaseModel]] = BusinessMessagesDeleted


class GuestMessageHandler(BaseHandler[TContext]):
    """Апдейты с полем `guest_message` (Message)."""

    update_field: ClassVar[str] = "guest_message"
    payload_type: ClassVar[type[BaseModel]] = Message


class MessageReactionHandler(BaseHandler[TContext]):
    """Апдейты с полем `message_reaction` (MessageReactionUpdated)."""

    update_field: ClassVar[str] = "message_reaction"
    payload_type: ClassVar[type[BaseModel]] = MessageReactionUpdated


class MessageReactionCountHandler(BaseHandler[TContext]):
    """Апдейты с полем `message_reaction_count` (MessageReactionCountUpdated)."""

    update_field: ClassVar[str] = "message_reaction_count"
    payload_type: ClassVar[type[BaseModel]] = MessageReactionCountUpdated


class InlineQueryHandler(BaseHandler[TContext]):
    """Апдейты с полем `inline_query` (InlineQuery)."""

    update_field: ClassVar[str] = "inline_query"
    payload_type: ClassVar[type[BaseModel]] = InlineQuery


class ChosenInlineResultHandler(BaseHandler[TContext]):
    """Апдейты с полем `chosen_inline_result` (ChosenInlineResult)."""

    update_field: ClassVar[str] = "chosen_inline_result"
    payload_type: ClassVar[type[BaseModel]] = ChosenInlineResult


class CallbackQueryHandler(BaseHandler[TContext]):
    """Апдейты с полем `callback_query` (CallbackQuery)."""

    update_field: ClassVar[str] = "callback_query"
    payload_type: ClassVar[type[BaseModel]] = CallbackQuery


class ShippingQueryHandler(BaseHandler[TContext]):
    """Апдейты с полем `shipping_query` (ShippingQuery)."""

    update_field: ClassVar[str] = "shipping_query"
    payload_type: ClassVar[type[BaseModel]] = ShippingQuery


class PreCheckoutQueryHandler(BaseHandler[TContext]):
    """Апдейты с полем `pre_checkout_query` (PreCheckoutQuery)."""

    update_field: ClassVar[str] = "pre_checkout_query"
    payload_type: ClassVar[type[BaseModel]] = PreCheckoutQuery


class PurchasedPaidMediaHandler(BaseHandler[TContext]):
    """Апдейты с полем `purchased_paid_media` (PaidMediaPurchased)."""

    update_field: ClassVar[str] = "purchased_paid_media"
    payload_type: ClassVar[type[BaseModel]] = PaidMediaPurchased


class PollHandler(BaseHandler[TContext]):
    """Апдейты с полем `poll` (Poll)."""

    update_field: ClassVar[str] = "poll"
    payload_type: ClassVar[type[BaseModel]] = Poll


class PollAnswerHandler(BaseHandler[TContext]):
    """Апдейты с полем `poll_answer` (PollAnswer)."""

    update_field: ClassVar[str] = "poll_answer"
    payload_type: ClassVar[type[BaseModel]] = PollAnswer


class MyChatMemberHandler(BaseHandler[TContext]):
    """Апдейты с полем `my_chat_member` (ChatMemberUpdated)."""

    update_field: ClassVar[str] = "my_chat_member"
    payload_type: ClassVar[type[BaseModel]] = ChatMemberUpdated


class ChatMemberHandler(BaseHandler[TContext]):
    """Апдейты с полем `chat_member` (ChatMemberUpdated)."""

    update_field: ClassVar[str] = "chat_member"
    payload_type: ClassVar[type[BaseModel]] = ChatMemberUpdated


class ChatJoinRequestHandler(BaseHandler[TContext]):
    """Апдейты с полем `chat_join_request` (ChatJoinRequest)."""

    update_field: ClassVar[str] = "chat_join_request"
    payload_type: ClassVar[type[BaseModel]] = ChatJoinRequest


class ChatBoostHandler(BaseHandler[TContext]):
    """Апдейты с полем `chat_boost` (ChatBoostUpdated)."""

    update_field: ClassVar[str] = "chat_boost"
    payload_type: ClassVar[type[BaseModel]] = ChatBoostUpdated


class RemovedChatBoostHandler(BaseHandler[TContext]):
    """Апдейты с полем `removed_chat_boost` (ChatBoostRemoved)."""

    update_field: ClassVar[str] = "removed_chat_boost"
    payload_type: ClassVar[type[BaseModel]] = ChatBoostRemoved


class ManagedBotHandler(BaseHandler[TContext]):
    """Апдейты с полем `managed_bot` (ManagedBotUpdated)."""

    update_field: ClassVar[str] = "managed_bot"
    payload_type: ClassVar[type[BaseModel]] = ManagedBotUpdated


class SubscriptionHandler(BaseHandler[TContext]):
    """Апдейты с полем `subscription` (BotSubscriptionUpdated)."""

    update_field: ClassVar[str] = "subscription"
    payload_type: ClassVar[type[BaseModel]] = BotSubscriptionUpdated


class StoppedMessageGenerationHandler(BaseHandler[TContext]):
    """Апдейты с полем `stopped_message_generation` (MessageGenerationStopped)."""

    update_field: ClassVar[str] = "stopped_message_generation"
    payload_type: ClassVar[type[BaseModel]] = MessageGenerationStopped


__all__ = [
    "MessageHandler",
    "EditedMessageHandler",
    "ChannelPostHandler",
    "EditedChannelPostHandler",
    "BusinessConnectionHandler",
    "BusinessMessageHandler",
    "EditedBusinessMessageHandler",
    "DeletedBusinessMessagesHandler",
    "GuestMessageHandler",
    "MessageReactionHandler",
    "MessageReactionCountHandler",
    "InlineQueryHandler",
    "ChosenInlineResultHandler",
    "CallbackQueryHandler",
    "ShippingQueryHandler",
    "PreCheckoutQueryHandler",
    "PurchasedPaidMediaHandler",
    "PollHandler",
    "PollAnswerHandler",
    "MyChatMemberHandler",
    "ChatMemberHandler",
    "ChatJoinRequestHandler",
    "ChatBoostHandler",
    "RemovedChatBoostHandler",
    "ManagedBotHandler",
    "SubscriptionHandler",
    "StoppedMessageGenerationHandler",
]
