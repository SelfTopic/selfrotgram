# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram Bot API 10.3, August 24, 2026.
# Руками не править — обновилась спека, перегенерировать.
# ruff: noqa
from __future__ import annotations

from typing import Generic, Optional, Union, cast

from typing_extensions import TypeVar

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
    Update,
)

Event = Union[Message, BusinessConnection, BusinessMessagesDeleted, MessageReactionUpdated, MessageReactionCountUpdated, InlineQuery, ChosenInlineResult, CallbackQuery, ShippingQuery, PreCheckoutQuery, PaidMediaPurchased, Poll, PollAnswer, ChatMemberUpdated, ChatJoinRequest, ChatBoostUpdated, ChatBoostRemoved, ManagedBotUpdated, BotSubscriptionUpdated, MessageGenerationStopped]

# Что обещает заголовок хендлера: AppContext[TextMessage],
# AppContext[DataCallbackQuery].
# По умолчанию — как раньше: сообщение, которое может отсутствовать.
TEvent = TypeVar("TEvent", covariant=True, default=Optional[Message])

_TMessage = TypeVar("_TMessage", bound=Optional[Message])
_TBusinessConnection = TypeVar("_TBusinessConnection", bound=Optional[BusinessConnection])
_TBusinessMessagesDeleted = TypeVar("_TBusinessMessagesDeleted", bound=Optional[BusinessMessagesDeleted])
_TMessageReactionUpdated = TypeVar("_TMessageReactionUpdated", bound=Optional[MessageReactionUpdated])
_TMessageReactionCountUpdated = TypeVar("_TMessageReactionCountUpdated", bound=Optional[MessageReactionCountUpdated])
_TInlineQuery = TypeVar("_TInlineQuery", bound=Optional[InlineQuery])
_TChosenInlineResult = TypeVar("_TChosenInlineResult", bound=Optional[ChosenInlineResult])
_TCallbackQuery = TypeVar("_TCallbackQuery", bound=Optional[CallbackQuery])
_TShippingQuery = TypeVar("_TShippingQuery", bound=Optional[ShippingQuery])
_TPreCheckoutQuery = TypeVar("_TPreCheckoutQuery", bound=Optional[PreCheckoutQuery])
_TPaidMediaPurchased = TypeVar("_TPaidMediaPurchased", bound=Optional[PaidMediaPurchased])
_TPoll = TypeVar("_TPoll", bound=Optional[Poll])
_TPollAnswer = TypeVar("_TPollAnswer", bound=Optional[PollAnswer])
_TChatMemberUpdated = TypeVar("_TChatMemberUpdated", bound=Optional[ChatMemberUpdated])
_TChatJoinRequest = TypeVar("_TChatJoinRequest", bound=Optional[ChatJoinRequest])
_TChatBoostUpdated = TypeVar("_TChatBoostUpdated", bound=Optional[ChatBoostUpdated])
_TChatBoostRemoved = TypeVar("_TChatBoostRemoved", bound=Optional[ChatBoostRemoved])
_TManagedBotUpdated = TypeVar("_TManagedBotUpdated", bound=Optional[ManagedBotUpdated])
_TBotSubscriptionUpdated = TypeVar("_TBotSubscriptionUpdated", bound=Optional[BotSubscriptionUpdated])
_TMessageGenerationStopped = TypeVar("_TMessageGenerationStopped", bound=Optional[MessageGenerationStopped])

_EVENT_FIELDS = (
    "message",
    "edited_message",
    "channel_post",
    "edited_channel_post",
    "business_connection",
    "business_message",
    "edited_business_message",
    "deleted_business_messages",
    "guest_message",
    "message_reaction",
    "message_reaction_count",
    "inline_query",
    "chosen_inline_result",
    "callback_query",
    "shipping_query",
    "pre_checkout_query",
    "purchased_paid_media",
    "poll",
    "poll_answer",
    "my_chat_member",
    "chat_member",
    "chat_join_request",
    "chat_boost",
    "removed_chat_boost",
    "managed_bot",
    "subscription",
    "stopped_message_generation",
)


class EventAccessors(Generic[TEvent]):
    """
    ctx.<поле Update> для каждого поля Update. Доступ типизирован через self:
    AppContext[TextMessage] даёт ctx.message: TextMessage, а
    ctx.callback_query
    в нём — ошибка типов. Без параметра — ctx.message: Optional[Message].
    Ограничение: message/edited_message/... делят один корневой тип, поэтому
    тип не отличает их между собой — берите поле своего вида обработчика.
    """

    update: Update

    @property
    def event(self) -> Optional[Event]:
        """Объект апдейта: заполнено не больше одного поля Update."""
        for name in _EVENT_FIELDS:
            value = getattr(self.update, name)
            if value is not None:
                return value

        return None

    @property
    def message(self: EventAccessors[_TMessage]) -> _TMessage:
        return cast(_TMessage, self.update.message)

    @property
    def edited_message(self: EventAccessors[_TMessage]) -> _TMessage:
        return cast(_TMessage, self.update.edited_message)

    @property
    def channel_post(self: EventAccessors[_TMessage]) -> _TMessage:
        return cast(_TMessage, self.update.channel_post)

    @property
    def edited_channel_post(self: EventAccessors[_TMessage]) -> _TMessage:
        return cast(_TMessage, self.update.edited_channel_post)

    @property
    def business_connection(self: EventAccessors[_TBusinessConnection]) -> _TBusinessConnection:
        return cast(_TBusinessConnection, self.update.business_connection)

    @property
    def business_message(self: EventAccessors[_TMessage]) -> _TMessage:
        return cast(_TMessage, self.update.business_message)

    @property
    def edited_business_message(self: EventAccessors[_TMessage]) -> _TMessage:
        return cast(_TMessage, self.update.edited_business_message)

    @property
    def deleted_business_messages(self: EventAccessors[_TBusinessMessagesDeleted]) -> _TBusinessMessagesDeleted:
        return cast(_TBusinessMessagesDeleted, self.update.deleted_business_messages)

    @property
    def guest_message(self: EventAccessors[_TMessage]) -> _TMessage:
        return cast(_TMessage, self.update.guest_message)

    @property
    def message_reaction(self: EventAccessors[_TMessageReactionUpdated]) -> _TMessageReactionUpdated:
        return cast(_TMessageReactionUpdated, self.update.message_reaction)

    @property
    def message_reaction_count(self: EventAccessors[_TMessageReactionCountUpdated]) -> _TMessageReactionCountUpdated:
        return cast(_TMessageReactionCountUpdated, self.update.message_reaction_count)

    @property
    def inline_query(self: EventAccessors[_TInlineQuery]) -> _TInlineQuery:
        return cast(_TInlineQuery, self.update.inline_query)

    @property
    def chosen_inline_result(self: EventAccessors[_TChosenInlineResult]) -> _TChosenInlineResult:
        return cast(_TChosenInlineResult, self.update.chosen_inline_result)

    @property
    def callback_query(self: EventAccessors[_TCallbackQuery]) -> _TCallbackQuery:
        return cast(_TCallbackQuery, self.update.callback_query)

    @property
    def shipping_query(self: EventAccessors[_TShippingQuery]) -> _TShippingQuery:
        return cast(_TShippingQuery, self.update.shipping_query)

    @property
    def pre_checkout_query(self: EventAccessors[_TPreCheckoutQuery]) -> _TPreCheckoutQuery:
        return cast(_TPreCheckoutQuery, self.update.pre_checkout_query)

    @property
    def purchased_paid_media(self: EventAccessors[_TPaidMediaPurchased]) -> _TPaidMediaPurchased:
        return cast(_TPaidMediaPurchased, self.update.purchased_paid_media)

    @property
    def poll(self: EventAccessors[_TPoll]) -> _TPoll:
        return cast(_TPoll, self.update.poll)

    @property
    def poll_answer(self: EventAccessors[_TPollAnswer]) -> _TPollAnswer:
        return cast(_TPollAnswer, self.update.poll_answer)

    @property
    def my_chat_member(self: EventAccessors[_TChatMemberUpdated]) -> _TChatMemberUpdated:
        return cast(_TChatMemberUpdated, self.update.my_chat_member)

    @property
    def chat_member(self: EventAccessors[_TChatMemberUpdated]) -> _TChatMemberUpdated:
        return cast(_TChatMemberUpdated, self.update.chat_member)

    @property
    def chat_join_request(self: EventAccessors[_TChatJoinRequest]) -> _TChatJoinRequest:
        return cast(_TChatJoinRequest, self.update.chat_join_request)

    @property
    def chat_boost(self: EventAccessors[_TChatBoostUpdated]) -> _TChatBoostUpdated:
        return cast(_TChatBoostUpdated, self.update.chat_boost)

    @property
    def removed_chat_boost(self: EventAccessors[_TChatBoostRemoved]) -> _TChatBoostRemoved:
        return cast(_TChatBoostRemoved, self.update.removed_chat_boost)

    @property
    def managed_bot(self: EventAccessors[_TManagedBotUpdated]) -> _TManagedBotUpdated:
        return cast(_TManagedBotUpdated, self.update.managed_bot)

    @property
    def subscription(self: EventAccessors[_TBotSubscriptionUpdated]) -> _TBotSubscriptionUpdated:
        return cast(_TBotSubscriptionUpdated, self.update.subscription)

    @property
    def stopped_message_generation(self: EventAccessors[_TMessageGenerationStopped]) -> _TMessageGenerationStopped:
        return cast(_TMessageGenerationStopped, self.update.stopped_message_generation)


__all__ = ["Event", "EventAccessors", "TEvent"]
