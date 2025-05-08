from typing import Optional, Self
from pydantic import BaseModel
from ..types import ChatMemberUpdated
from ..types import PollAnswer
from ..types import CallbackQuery
from ..types import ChatJoinRequest
from ..payments import PreCheckoutQuery
from ..types import Message
from ..types import BusinessConnection
from ..types import BusinessMessagesDeleted
from .inline_query import InlineQuery
from .chosen_inline_result import ChosenInlineResult
from ..types import ChatBoostUpdated
from ..types import Poll
from ..types import ChatBoostRemoved
from ..types import MessageReactionCountUpdated
from ..payments import PaidMediaPurchased
from ..types import MessageReactionUpdated
from ..payments import ShippingQuery

class Update(BaseModel):
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    business_connection: Optional[BusinessConnection] = None
    business_message: Optional[Message] = None
    edited_business_message: Optional[Message] = None
    deleted_business_messages: Optional[BusinessMessagesDeleted] = None
    message_reaction: Optional[MessageReactionUpdated] = None
    message_reaction_count: Optional[MessageReactionCountUpdated] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    callback_query: Optional[CallbackQuery] = None
    shipping_query: Optional[ShippingQuery] = None
    pre_checkout_query: Optional[PreCheckoutQuery] = None
    purchased_paid_media: Optional[PaidMediaPurchased] = None
    poll: Optional[Poll] = None
    poll_answer: Optional[PollAnswer] = None
    my_chat_member: Optional[ChatMemberUpdated] = None
    chat_member: Optional[ChatMemberUpdated] = None
    chat_join_request: Optional[ChatJoinRequest] = None
    chat_boost: Optional[ChatBoostUpdated] = None
    removed_chat_boost: Optional[ChatBoostRemoved] = None