
# class: start
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
# class: end

# class: start
@dataclass
class GetUpdates(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getUpdates"
    offset: Optional[int] = None
    limit: Optional[int] = None
    timeout: Optional[int] = None
    allowed_updates: Optional[List[str]] = None
# class: end

# class: start
@dataclass
class SetWebhook(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setWebhook"
    url: str
    certificate: Optional[InputFile] = None
    ip_address: Optional[str] = None
    max_connections: Optional[int] = None
    allowed_updates: Optional[List[str]] = None
    drop_pending_updates: Optional[bool] = None
    secret_token: Optional[str] = None
# class: end

# class: start
@dataclass
class DeleteWebhook(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteWebhook"
    drop_pending_updates: Optional[bool] = None
# class: end

# class: start
@dataclass
class GetWebhookInfo(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getWebhookInfo"
# class: end

# class: start
class WebhookInfo(BaseModel):
    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: Optional[str] = None
    last_error_date: Optional[int] = None
    last_error_message: Optional[str] = None
    last_synchronization_error_date: Optional[int] = None
    max_connections: Optional[int] = None
    allowed_updates: Optional[List[str]] = None
# class: end
