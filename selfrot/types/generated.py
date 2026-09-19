# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram Bot API 10.3, August 24, 2026.
# Руками не править — обновилась спека, перегенерировать.
# ruff: noqa
from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Discriminator, Field, PrivateAttr, Tag
from typing_extensions import TypeAliasType

from ..exceptions import BotNotBoundError
from .input_file import InputFile

if TYPE_CHECKING:
    from ..client.methods import BotMethods


class _Base(BaseModel, frozen=True):
    # protected_namespaces=(): в Bot API есть поле model_custom_emoji_id.
    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())

    # Бот, с которым объект получен (Bot.call и вебхук передают его в контексте
    # валидации). Нужен методам на объектах: message.answer(...), callback.answer().
    _bot: Any = PrivateAttr(default=None)

    def model_post_init(self, context: Any, /) -> None:
        # Модель frozen, поэтому не self._bot = ..., а напрямую в приватное хранилище.
        private = self.__pydantic_private__
        if private is not None and isinstance(context, dict):
            if context.get("bot") is not None:
                private["_bot"] = context["bot"]

    def _require_bot(self) -> BotMethods:
        if self._bot is None:
            raise BotNotBoundError(
                f"{type(self).__name__} не привязан к боту: объект создан вручную или "
                "разобран без контекста {'bot': ...}. Вызовите метод у бота напрямую"
            )
        return self._bot


RichText = TypeAliasType("RichText", Union[str, List["RichText"], "RichTextBold", "RichTextItalic", "RichTextUnderline", "RichTextStrikethrough", "RichTextSpoiler", "RichTextDateTime", "RichTextTextMention", "RichTextSubscript", "RichTextSuperscript", "RichTextMarked", "RichTextCode", "RichTextCustomEmoji", "RichTextMathematicalExpression", "RichTextUrl", "RichTextEmailAddress", "RichTextPhoneNumber", "RichTextBankCardNumber", "RichTextMention", "RichTextHashtag", "RichTextCashtag", "RichTextBotCommand", "RichTextButton", "RichTextAnchor", "RichTextAnchorLink", "RichTextReference", "RichTextReferenceLink"])

class Update(_Base, frozen=True):
    """This object represents an incoming update.
    
    At most one of the optional fields can be present in any given update.
    
    https://core.telegram.org/bots/api#update
    """
    update_id: int
    """The update's unique identifier. Update identifiers start from a certain positive number and increase sequentially. This identifier becomes especially handy if you're using webhooks, since it allows you to ignore repeated updates or to restore the correct update sequence, should they get out of order. If there are no new updates for at least a week, then identifier of the next update will be chosen randomly instead of sequentially."""
    message: Optional[Message] = Field(default=None)
    """Optional. New incoming message of any kind - text, photo, sticker, etc."""
    edited_message: Optional[Message] = Field(default=None)
    """Optional. New version of a message that is known to the bot and was edited. This update may at times be triggered by changes to message fields that are either unavailable or not actively used by your bot."""
    channel_post: Optional[Message] = Field(default=None)
    """Optional. New incoming channel post of any kind - text, photo, sticker, etc."""
    edited_channel_post: Optional[Message] = Field(default=None)
    """Optional. New version of a channel post that is known to the bot and was edited. This update may at times be triggered by changes to message fields that are either unavailable or not actively used by your bot."""
    business_connection: Optional[BusinessConnection] = Field(default=None)
    """Optional. The bot was connected to or disconnected from a business account, or a user edited an existing connection with the bot"""
    business_message: Optional[Message] = Field(default=None)
    """Optional. New message from a connected business account"""
    edited_business_message: Optional[Message] = Field(default=None)
    """Optional. New version of a message from a connected business account"""
    deleted_business_messages: Optional[BusinessMessagesDeleted] = Field(default=None)
    """Optional. Messages were deleted from a connected business account"""
    guest_message: Optional[Message] = Field(default=None)
    """Optional. New guest message. The bot can use the field Message.guest_query_id and the method answerGuestQuery to send a message in response."""
    message_reaction: Optional[MessageReactionUpdated] = Field(default=None)
    """Optional. A reaction to a message was changed by a user. The bot must be an administrator in the chat and must explicitly specify "message_reaction" in the list of allowed_updates to receive these updates. The update isn't received for reactions set by bots."""
    message_reaction_count: Optional[MessageReactionCountUpdated] = Field(default=None)
    """Optional. Reactions to a message with anonymous reactions were changed. The bot must be an administrator in the chat and must explicitly specify "message_reaction_count" in the list of allowed_updates to receive these updates. The updates are grouped and can be sent with delay up to a few minutes."""
    inline_query: Optional[InlineQuery] = Field(default=None)
    """Optional. New incoming inline query"""
    chosen_inline_result: Optional[ChosenInlineResult] = Field(default=None)
    """Optional. The result of an inline query that was chosen by a user and sent to their chat partner. Please see our documentation on the feedback collecting for details on how to enable these updates for your bot."""
    callback_query: Optional[CallbackQuery] = Field(default=None)
    """Optional. New incoming callback query"""
    shipping_query: Optional[ShippingQuery] = Field(default=None)
    """Optional. New incoming shipping query. Only for invoices with flexible price."""
    pre_checkout_query: Optional[PreCheckoutQuery] = Field(default=None)
    """Optional. New incoming pre-checkout query. Contains full information about checkout."""
    purchased_paid_media: Optional[PaidMediaPurchased] = Field(default=None)
    """Optional. A user purchased paid media with a non-empty payload sent by the bot in a non-channel chat"""
    poll: Optional[Poll] = Field(default=None)
    """Optional. New poll state. Bots receive only updates about manually stopped polls and polls, which are sent by the bot."""
    poll_answer: Optional[PollAnswer] = Field(default=None)
    """Optional. A user changed their answer in a non-anonymous poll. Bots receive new votes only in polls that were sent by the bot itself."""
    my_chat_member: Optional[ChatMemberUpdated] = Field(default=None)
    """Optional. The bot's chat member status was updated in a chat. For private chats, this update is received only when the bot is blocked or unblocked by the user."""
    chat_member: Optional[ChatMemberUpdated] = Field(default=None)
    """Optional. A chat member's status was updated in a chat. The bot must be an administrator in the chat and must explicitly specify "chat_member" in the list of allowed_updates to receive these updates."""
    chat_join_request: Optional[ChatJoinRequest] = Field(default=None)
    """Optional. A request to join the chat has been sent. The bot must have the can_invite_users administrator right in the chat to receive these updates."""
    chat_boost: Optional[ChatBoostUpdated] = Field(default=None)
    """Optional. A chat boost was added or changed. The bot must be an administrator in the chat to receive these updates."""
    removed_chat_boost: Optional[ChatBoostRemoved] = Field(default=None)
    """Optional. A boost was removed from a chat. The bot must be an administrator in the chat to receive these updates."""
    managed_bot: Optional[ManagedBotUpdated] = Field(default=None)
    """Optional. A new bot was created to be managed by the bot, or token or owner of a managed bot was changed"""
    subscription: Optional[BotSubscriptionUpdated] = Field(default=None)
    """Optional. User payment subscription has changed"""
    stopped_message_generation: Optional[MessageGenerationStopped] = Field(default=None)
    """Optional. A user asked the bot to stop the generation of a message"""

class WebhookInfo(_Base, frozen=True):
    """Describes the current status of a webhook.
    
    https://core.telegram.org/bots/api#webhookinfo
    """
    url: str
    """Webhook URL, may be empty if webhook is not set up"""
    has_custom_certificate: bool
    """True, if a custom certificate was provided for webhook certificate checks"""
    pending_update_count: int
    """Number of updates awaiting delivery"""
    ip_address: Optional[str] = Field(default=None)
    """Optional. Currently used webhook IP address"""
    last_error_date: Optional[int] = Field(default=None)
    """Optional. Unix time for the most recent error that happened when trying to deliver an update via webhook"""
    last_error_message: Optional[str] = Field(default=None)
    """Optional. Error message in human-readable format for the most recent error that happened when trying to deliver an update via webhook"""
    last_synchronization_error_date: Optional[int] = Field(default=None)
    """Optional. Unix time of the most recent error that happened when trying to synchronize available updates with Telegram datacenters"""
    max_connections: Optional[int] = Field(default=None)
    """Optional. The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery"""
    allowed_updates: Optional[List[str]] = Field(default=None)
    """Optional. A list of update types the bot is subscribed to. Defaults to all update types except chat_member, message_reaction, and message_reaction_count."""

class User(_Base, frozen=True):
    """This object represents a Telegram user or bot.
    
    https://core.telegram.org/bots/api#user
    """
    id: int
    """Unique identifier for this user or bot. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier."""
    is_bot: bool
    """True, if this user is a bot"""
    first_name: str
    """User's or bot's first name"""
    last_name: Optional[str] = Field(default=None)
    """Optional. User's or bot's last name"""
    username: Optional[str] = Field(default=None)
    """Optional. User's or bot's username"""
    language_code: Optional[str] = Field(default=None)
    """Optional. IETF language tag of the user's language"""
    is_premium: Optional[bool] = Field(default=None)
    """Optional. True, if this user is a Telegram Premium user"""
    added_to_attachment_menu: Optional[bool] = Field(default=None)
    """Optional. True, if this user added the bot to the attachment menu"""
    can_join_groups: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can be invited to groups. Returned only in getMe."""
    can_read_all_group_messages: Optional[bool] = Field(default=None)
    """Optional. True, if privacy mode is disabled for the bot. Returned only in getMe."""
    supports_guest_queries: Optional[bool] = Field(default=None)
    """Optional. True, if the bot supports guest queries from chats it is not a member of. Returned only in getMe."""
    supports_inline_queries: Optional[bool] = Field(default=None)
    """Optional. True, if the bot supports inline queries. Returned only in getMe."""
    can_connect_to_business: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can be connected to a user account to manage it. Returned only in getMe."""
    has_main_web_app: Optional[bool] = Field(default=None)
    """Optional. True, if the bot has a main Web App. Returned only in getMe."""
    has_topics_enabled: Optional[bool] = Field(default=None)
    """Optional. True, if the bot has forum topic mode enabled in private chats. Returned only in getMe."""
    allows_users_to_create_topics: Optional[bool] = Field(default=None)
    """Optional. True, if the bot allows users to create and delete topics in private chats. Returned only in getMe."""
    can_manage_bots: Optional[bool] = Field(default=None)
    """Optional. True, if other bots can be created to be controlled by the bot. Returned only in getMe."""
    supports_join_request_queries: Optional[bool] = Field(default=None)
    """Optional. True, if the bot supports join request queries and can be assigned to process them. Returned only in getMe."""

class Chat(_Base, frozen=True):
    """This object represents a chat.
    
    https://core.telegram.org/bots/api#chat
    """
    id: int
    """Unique identifier for this chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier."""
    type: str
    """Type of the chat, can be either "private", "group", "supergroup" or "channel" """
    title: Optional[str] = Field(default=None)
    """Optional. Title, for supergroups, channels and group chats"""
    username: Optional[str] = Field(default=None)
    """Optional. Username, for private chats, supergroups and channels if available"""
    first_name: Optional[str] = Field(default=None)
    """Optional. First name of the other party in a private chat"""
    last_name: Optional[str] = Field(default=None)
    """Optional. Last name of the other party in a private chat"""
    is_forum: Optional[bool] = Field(default=None)
    """Optional. True, if the supergroup chat is a forum (has topics enabled)"""
    is_direct_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the chat is the direct messages chat of a channel"""

class ChatFullInfo(_Base, frozen=True):
    """This object contains full information about a chat.
    
    https://core.telegram.org/bots/api#chatfullinfo
    """
    id: int
    """Unique identifier for this chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier."""
    type: str
    """Type of the chat, can be either "private", "group", "supergroup" or "channel" """
    title: Optional[str] = Field(default=None)
    """Optional. Title, for supergroups, channels and group chats"""
    username: Optional[str] = Field(default=None)
    """Optional. Username, for private chats, supergroups and channels if available"""
    first_name: Optional[str] = Field(default=None)
    """Optional. First name of the other party in a private chat"""
    last_name: Optional[str] = Field(default=None)
    """Optional. Last name of the other party in a private chat"""
    is_forum: Optional[bool] = Field(default=None)
    """Optional. True, if the supergroup chat is a forum (has topics enabled)"""
    is_direct_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the chat is the direct messages chat of a channel"""
    accent_color_id: int
    """Identifier of the accent color for the chat name and backgrounds of the chat photo, reply header, and link preview. See accent colors for more details."""
    max_reaction_count: int
    """The maximum number of reactions that can be set on a message in the chat"""
    photo: Optional[ChatPhoto] = Field(default=None)
    """Optional. Chat photo"""
    active_usernames: Optional[List[str]] = Field(default=None)
    """Optional. If non-empty, the list of all active chat usernames; for private chats, supergroups and channels"""
    birthdate: Optional[Birthdate] = Field(default=None)
    """Optional. For private chats, the date of birth of the user"""
    business_intro: Optional[BusinessIntro] = Field(default=None)
    """Optional. For private chats with business accounts, the intro of the business"""
    business_location: Optional[BusinessLocation] = Field(default=None)
    """Optional. For private chats with business accounts, the location of the business"""
    business_opening_hours: Optional[BusinessOpeningHours] = Field(default=None)
    """Optional. For private chats with business accounts, the opening hours of the business"""
    personal_chat: Optional[Chat] = Field(default=None)
    """Optional. For private chats, the personal channel of the user"""
    parent_chat: Optional[Chat] = Field(default=None)
    """Optional. Information about the corresponding channel chat; for direct messages chats only"""
    available_reactions: Optional[List[ReactionType]] = Field(default=None)
    """Optional. List of available reactions allowed in the chat. If omitted, then all emoji reactions are allowed."""
    background_custom_emoji_id: Optional[str] = Field(default=None)
    """Optional. Custom emoji identifier of the emoji chosen by the chat for the reply header and link preview background"""
    profile_accent_color_id: Optional[int] = Field(default=None)
    """Optional. Identifier of the accent color for the chat's profile background. See profile accent colors for more details."""
    profile_background_custom_emoji_id: Optional[str] = Field(default=None)
    """Optional. Custom emoji identifier of the emoji chosen by the chat for its profile background"""
    emoji_status_custom_emoji_id: Optional[str] = Field(default=None)
    """Optional. Custom emoji identifier of the emoji status of the chat or the other party in a private chat"""
    emoji_status_expiration_date: Optional[int] = Field(default=None)
    """Optional. Expiration date of the emoji status of the chat or the other party in a private chat, in Unix time, if any"""
    bio: Optional[str] = Field(default=None)
    """Optional. Bio of the other party in a private chat"""
    has_private_forwards: Optional[bool] = Field(default=None)
    """Optional. True, if privacy settings of the other party in the private chat allows to use tg://user?id=<user_id> links only in chats with the user"""
    has_restricted_voice_and_video_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the privacy settings of the other party restrict sending voice and video note messages in the private chat"""
    join_to_send_messages: Optional[bool] = Field(default=None)
    """Optional. True, if users need to join the supergroup before they can send messages"""
    join_by_request: Optional[bool] = Field(default=None)
    """Optional. True, if all users directly joining the supergroup without using an invite link need to be approved by supergroup administrators"""
    description: Optional[str] = Field(default=None)
    """Optional. Description, for groups, supergroups and channel chats"""
    invite_link: Optional[str] = Field(default=None)
    """Optional. Primary invite link, for groups, supergroups and channel chats"""
    pinned_message: Optional[Message] = Field(default=None)
    """Optional. The most recent pinned message (by sending date)"""
    permissions: Optional[ChatPermissions] = Field(default=None)
    """Optional. Default chat member permissions, for groups and supergroups"""
    accepted_gift_types: AcceptedGiftTypes
    """Information about types of gifts that are accepted by the chat or by the corresponding user for private chats"""
    can_send_paid_media: Optional[bool] = Field(default=None)
    """Optional. True, if paid media messages can be sent or forwarded to the channel chat. The field is available only for channel chats."""
    slow_mode_delay: Optional[int] = Field(default=None)
    """Optional. For supergroups, the minimum allowed delay between consecutive messages sent by each unprivileged user; in seconds"""
    unrestrict_boost_count: Optional[int] = Field(default=None)
    """Optional. For supergroups, the minimum number of boosts that a non-administrator user needs to add in order to ignore slow mode and chat permissions"""
    message_auto_delete_time: Optional[int] = Field(default=None)
    """Optional. The time after which all messages sent to the chat will be automatically deleted; in seconds"""
    has_aggressive_anti_spam_enabled: Optional[bool] = Field(default=None)
    """Optional. True, if aggressive anti-spam checks are enabled in the supergroup. The field is only available to chat administrators."""
    has_hidden_members: Optional[bool] = Field(default=None)
    """Optional. True, if non-administrators can only get the list of bots and administrators in the chat"""
    has_protected_content: Optional[bool] = Field(default=None)
    """Optional. True, if messages from the chat can't be forwarded to other chats"""
    has_visible_history: Optional[bool] = Field(default=None)
    """Optional. True, if new chat members will have access to old messages; available only to chat administrators"""
    sticker_set_name: Optional[str] = Field(default=None)
    """Optional. For supergroups, name of the group sticker set"""
    can_set_sticker_set: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can change the group sticker set"""
    custom_emoji_sticker_set_name: Optional[str] = Field(default=None)
    """Optional. For supergroups, the name of the group's custom emoji sticker set. Custom emoji from this set can be used by all users and bots in the group."""
    linked_chat_id: Optional[int] = Field(default=None)
    """Optional. Unique identifier for the linked chat, i.e. the discussion group identifier for a channel and vice versa; for supergroups and channel chats. This identifier may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier."""
    location: Optional[ChatLocation] = Field(default=None)
    """Optional. For supergroups, the location to which the supergroup is connected"""
    rating: Optional[UserRating] = Field(default=None)
    """Optional. For private chats, the rating of the user if any"""
    first_profile_audio: Optional[Audio] = Field(default=None)
    """Optional. For private chats, the first audio added to the profile of the user"""
    unique_gift_colors: Optional[UniqueGiftColors] = Field(default=None)
    """Optional. The color scheme based on a unique gift that must be used for the chat's name, message replies and link previews"""
    paid_message_star_count: Optional[int] = Field(default=None)
    """Optional. The number of Telegram Stars a general user has to pay to send a message to the chat"""
    guard_bot: Optional[User] = Field(default=None)
    """Optional. The bot that processes join request queries in the chat. The field is only available to chat administrators."""
    community: Optional[Community] = Field(default=None)
    """Optional. The Community to which the chat belongs"""

class Message(_Base, frozen=True):
    """This object represents a message.
    
    https://core.telegram.org/bots/api#message
    """
    message_id: int
    """Unique message identifier inside this chat; 0 for ephemeral messages. In specific instances (e.g., a message containing a video sent to a big chat), the server might automatically schedule a message instead of sending it immediately. In such cases, this field will be 0 and the relevant message will be unusable until it is actually sent."""
    message_thread_id: Optional[int] = Field(default=None)
    """Optional. Unique identifier of a message thread or forum topic to which the message belongs; for supergroups and private chats only"""
    direct_messages_topic: Optional[DirectMessagesTopic] = Field(default=None)
    """Optional. Information about the direct messages chat topic that contains the message"""
    user: Optional[User] = Field(default=None, alias='from')
    """Optional. Sender of the message; may be empty for messages sent to channels. For backward compatibility, if the message was sent on behalf of a chat, the field contains a fake sender user in non-channel chats."""
    sender_chat: Optional[Chat] = Field(default=None)
    """Optional. Sender of the message when sent on behalf of a chat. For example, the supergroup itself for messages sent by its anonymous administrators or a linked channel for messages automatically forwarded to the channel's discussion group. For backward compatibility, if the message was sent on behalf of a chat, the field from contains a fake sender user in non-channel chats."""
    sender_boost_count: Optional[int] = Field(default=None)
    """Optional. If the sender of the message boosted the chat, the number of boosts added by the user"""
    sender_business_bot: Optional[User] = Field(default=None)
    """Optional. The bot that actually sent the message on behalf of the business account. Available only for outgoing messages sent on behalf of the connected business account."""
    sender_tag: Optional[str] = Field(default=None)
    """Optional. Tag or custom title of the sender of the message; for supergroups only"""
    receiver_user: Optional[User] = Field(default=None)
    """Optional. For ephemeral messages, the user who received the message"""
    ephemeral_message_id: Optional[int] = Field(default=None)
    """Optional. For ephemeral messages, identifier of the ephemeral message inside this chat. The identifier may be reused for another ephemeral message after the message is deleted or expires."""
    date: int
    """Date the message was sent in Unix time. It is always a positive number, representing a valid date."""
    guest_query_id: Optional[str] = Field(default=None)
    """Optional. The unique identifier for the guest query. Use this identifier with the method answerGuestQuery to send a response message. If non-empty, the message belongs to the chat where the guest bot was summoned, which may not coincide with other existing bot chats sharing the same identifier."""
    business_connection_id: Optional[str] = Field(default=None)
    """Optional. Unique identifier of the business connection from which the message was received. If non-empty, the message belongs to a chat of the corresponding business account that is independent from any potential bot chat which might share the same identifier."""
    chat: Chat
    """Chat the message belongs to"""
    forward_origin: Optional[MessageOrigin] = Field(default=None)
    """Optional. Information about the original message for forwarded messages"""
    is_topic_message: Optional[bool] = Field(default=None)
    """Optional. True, if the message is sent to a topic in a forum supergroup or a private chat with the bot"""
    is_automatic_forward: Optional[bool] = Field(default=None)
    """Optional. True, if the message is a channel post that was automatically forwarded to the connected discussion group"""
    reply_to_message: Optional[Message] = Field(default=None)
    """Optional. For replies in the same chat and message thread, the original message. Note that the Message object in this field will not contain further reply_to_message fields even if it itself is a reply. If the message is a reply to an ephemeral message, then this field may be omitted."""
    external_reply: Optional[ExternalReplyInfo] = Field(default=None)
    """Optional. Information about the message that is being replied to, which may come from another chat or forum topic"""
    quote: Optional[TextQuote] = Field(default=None)
    """Optional. For replies that quote part of the original message, the quoted part of the message"""
    reply_to_story: Optional[Story] = Field(default=None)
    """Optional. For replies to a story, the original story"""
    reply_to_checklist_task_id: Optional[int] = Field(default=None)
    """Optional. Identifier of the specific checklist task that is being replied to"""
    reply_to_poll_option_id: Optional[str] = Field(default=None)
    """Optional. Persistent identifier of the specific poll option that is being replied to"""
    via_bot: Optional[User] = Field(default=None)
    """Optional. Bot through which the message was sent"""
    guest_bot_caller_user: Optional[User] = Field(default=None)
    """Optional. For a message sent by a guest bot, this is the user whose original message triggered the bot's response"""
    guest_bot_caller_chat: Optional[Chat] = Field(default=None)
    """Optional. For a message sent by a guest bot, this is the chat whose original message triggered the bot's response"""
    edit_date: Optional[int] = Field(default=None)
    """Optional. Date the message was last edited in Unix time"""
    has_protected_content: Optional[bool] = Field(default=None)
    """Optional. True, if the message can't be forwarded"""
    is_from_offline: Optional[bool] = Field(default=None)
    """Optional. True, if the message was sent by an implicit action, for example, as an away or a greeting business message, or as a scheduled message"""
    is_paid_post: Optional[bool] = Field(default=None)
    """Optional. True, if the message is a paid post. Note that such posts must not be deleted for 24 hours to receive the payment and can't be edited."""
    media_group_id: Optional[str] = Field(default=None)
    """Optional. The unique identifier inside this chat of a media message group this message belongs to"""
    author_signature: Optional[str] = Field(default=None)
    """Optional. Signature of the post author for messages in channels, or the custom title of an anonymous group administrator"""
    paid_star_count: Optional[int] = Field(default=None)
    """Optional. The number of Telegram Stars that were paid by the sender of the message to send it"""
    text: Optional[str] = Field(default=None)
    """Optional. For text messages, the actual UTF-8 text of the message"""
    entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text"""
    link_preview_options: Optional[LinkPreviewOptions] = Field(default=None)
    """Optional. Options used for link preview generation for the message, if it is a text message and link preview options were changed"""
    suggested_post_info: Optional[SuggestedPostInfo] = Field(default=None)
    """Optional. Information about suggested post parameters if the message is a suggested post in a channel direct messages chat. If the message is an approved or declined suggested post, then it can't be edited."""
    effect_id: Optional[str] = Field(default=None)
    """Optional. Unique identifier of the message effect added to the message"""
    rich_message: Optional[RichMessage] = Field(default=None)
    """Optional. Message is a rich formatted message"""
    animation: Optional[Animation] = Field(default=None)
    """Optional. Message is an animation, information about the animation. For backward compatibility, when this field is set, the document field will also be set."""
    audio: Optional[Audio] = Field(default=None)
    """Optional. Message is an audio file, information about the file"""
    document: Optional[Document] = Field(default=None)
    """Optional. Message is a general file, information about the file"""
    live_photo: Optional[LivePhoto] = Field(default=None)
    """Optional. Message is a live photo, information about the live photo. For backward compatibility, when this field is set, the photo field will also be set."""
    paid_media: Optional[PaidMediaInfo] = Field(default=None)
    """Optional. Message contains paid media; information about the paid media"""
    photo: Optional[List[PhotoSize]] = Field(default=None)
    """Optional. Message is a photo, available sizes of the photo"""
    sticker: Optional[Sticker] = Field(default=None)
    """Optional. Message is a sticker, information about the sticker"""
    story: Optional[Story] = Field(default=None)
    """Optional. Message is a forwarded story"""
    video: Optional[Video] = Field(default=None)
    """Optional. Message is a video, information about the video"""
    video_note: Optional[VideoNote] = Field(default=None)
    """Optional. Message is a video note, information about the video message"""
    voice: Optional[Voice] = Field(default=None)
    """Optional. Message is a voice message, information about the file"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption for the animation, audio, document, paid media, photo, video or voice"""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear in the caption"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. True, if the caption must be shown above the message media"""
    has_media_spoiler: Optional[bool] = Field(default=None)
    """Optional. True, if the message media is covered by a spoiler animation"""
    checklist: Optional[Checklist] = Field(default=None)
    """Optional. Message is a checklist"""
    contact: Optional[Contact] = Field(default=None)
    """Optional. Message is a shared contact, information about the contact"""
    dice: Optional[Dice] = Field(default=None)
    """Optional. Message is a dice with random value"""
    game: Optional[Game] = Field(default=None)
    """Optional. Message is a game, information about the game. More about games: https://core.telegram.org/bots/api#games"""
    poll: Optional[Poll] = Field(default=None)
    """Optional. Message is a native poll, information about the poll"""
    venue: Optional[Venue] = Field(default=None)
    """Optional. Message is a venue, information about the venue. For backward compatibility, when this field is set, the location field will also be set."""
    location: Optional[Location] = Field(default=None)
    """Optional. Message is a shared location, information about the location"""
    new_chat_members: Optional[List[User]] = Field(default=None)
    """Optional. New members that were added to the group or supergroup and information about them (the bot itself may be one of these members)"""
    left_chat_member: Optional[User] = Field(default=None)
    """Optional. A member was removed from the group, information about them (this member may be the bot itself)"""
    chat_owner_left: Optional[ChatOwnerLeft] = Field(default=None)
    """Optional. Service message: chat owner has left"""
    chat_owner_changed: Optional[ChatOwnerChanged] = Field(default=None)
    """Optional. Service message: chat owner has changed"""
    new_chat_title: Optional[str] = Field(default=None)
    """Optional. A chat title was changed to this value"""
    new_chat_photo: Optional[List[PhotoSize]] = Field(default=None)
    """Optional. A chat photo was change to this value"""
    delete_chat_photo: Optional[bool] = Field(default=None)
    """Optional. Service message: the chat photo was deleted"""
    group_chat_created: Optional[bool] = Field(default=None)
    """Optional. Service message: the group has been created"""
    supergroup_chat_created: Optional[bool] = Field(default=None)
    """Optional. Service message: the supergroup has been created. This field can't be received in a message coming through updates, because bot can't be a member of a supergroup when it is created. It can only be found in reply_to_message if someone replies to a very first message in a directly created supergroup."""
    channel_chat_created: Optional[bool] = Field(default=None)
    """Optional. Service message: the channel has been created. This field can't be received in a message coming through updates, because bot can't be a member of a channel when it is created. It can only be found in reply_to_message if someone replies to a very first message in a channel."""
    message_auto_delete_timer_changed: Optional[MessageAutoDeleteTimerChanged] = Field(default=None)
    """Optional. Service message: auto-delete timer settings changed in the chat"""
    migrate_to_chat_id: Optional[int] = Field(default=None)
    """Optional. The group has been migrated to a supergroup with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier."""
    migrate_from_chat_id: Optional[int] = Field(default=None)
    """Optional. The supergroup has been migrated from a group with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier."""
    pinned_message: Optional[MaybeInaccessibleMessage] = Field(default=None)
    """Optional. Specified message was pinned. Note that the Message object in this field will not contain further reply_to_message fields even if it itself is a reply."""
    invoice: Optional[Invoice] = Field(default=None)
    """Optional. Message is an invoice for a payment, information about the invoice. More about payments: https://core.telegram.org/bots/api#payments"""
    successful_payment: Optional[SuccessfulPayment] = Field(default=None)
    """Optional. Message is a service message about a successful payment, information about the payment. More about payments: https://core.telegram.org/bots/api#payments"""
    refunded_payment: Optional[RefundedPayment] = Field(default=None)
    """Optional. Message is a service message about a refunded payment, information about the payment. More about payments: https://core.telegram.org/bots/api#payments"""
    users_shared: Optional[UsersShared] = Field(default=None)
    """Optional. Service message: users were shared with the bot"""
    chat_shared: Optional[ChatShared] = Field(default=None)
    """Optional. Service message: a chat was shared with the bot"""
    gift: Optional[GiftInfo] = Field(default=None)
    """Optional. Service message: a regular gift was sent or received"""
    unique_gift: Optional[UniqueGiftInfo] = Field(default=None)
    """Optional. Service message: a unique gift was sent or received"""
    gift_upgrade_sent: Optional[GiftInfo] = Field(default=None)
    """Optional. Service message: upgrade of a gift was purchased after the gift was sent"""
    connected_website: Optional[str] = Field(default=None)
    """Optional. The domain name of the website on which the user has logged in. More about Telegram Login: https://core.telegram.org/widgets/login"""
    write_access_allowed: Optional[WriteAccessAllowed] = Field(default=None)
    """Optional. Service message: the user allowed the bot to write messages after adding it to the attachment or side menu, launching a Web App from a link, or accepting an explicit request from a Web App sent by the method requestWriteAccess"""
    passport_data: Optional[PassportData] = Field(default=None)
    """Optional. Telegram Passport data"""
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = Field(default=None)
    """Optional. Service message: a user in the chat triggered another user's proximity alert while sharing Live Location"""
    boost_added: Optional[ChatBoostAdded] = Field(default=None)
    """Optional. Service message: user boosted the chat"""
    chat_background_set: Optional[ChatBackground] = Field(default=None)
    """Optional. Service message: chat background set"""
    checklist_tasks_done: Optional[ChecklistTasksDone] = Field(default=None)
    """Optional. Service message: some tasks in a checklist were marked as done or not done"""
    checklist_tasks_added: Optional[ChecklistTasksAdded] = Field(default=None)
    """Optional. Service message: tasks were added to a checklist"""
    community_chat_added: Optional[CommunityChatAdded] = Field(default=None)
    """Optional. Service message: chat or bot added to a Community"""
    community_chat_joined: Optional[CommunityChatJoined] = Field(default=None)
    """Optional. Service message: chat was joined by a user from a Community"""
    community_chat_removed: Optional[CommunityChatRemoved] = Field(default=None)
    """Optional. Service message: chat or bot removed from a Community"""
    direct_message_price_changed: Optional[DirectMessagePriceChanged] = Field(default=None)
    """Optional. Service message: the price for paid messages in the corresponding direct messages chat of a channel has changed"""
    forum_topic_created: Optional[ForumTopicCreated] = Field(default=None)
    """Optional. Service message: forum topic created"""
    forum_topic_edited: Optional[ForumTopicEdited] = Field(default=None)
    """Optional. Service message: forum topic edited"""
    forum_topic_closed: Optional[ForumTopicClosed] = Field(default=None)
    """Optional. Service message: forum topic closed"""
    forum_topic_reopened: Optional[ForumTopicReopened] = Field(default=None)
    """Optional. Service message: forum topic reopened"""
    general_forum_topic_hidden: Optional[GeneralForumTopicHidden] = Field(default=None)
    """Optional. Service message: the 'General' forum topic hidden"""
    general_forum_topic_unhidden: Optional[GeneralForumTopicUnhidden] = Field(default=None)
    """Optional. Service message: the 'General' forum topic unhidden"""
    giveaway_created: Optional[GiveawayCreated] = Field(default=None)
    """Optional. Service message: a scheduled giveaway was created"""
    giveaway: Optional[Giveaway] = Field(default=None)
    """Optional. The message is a scheduled giveaway message"""
    giveaway_winners: Optional[GiveawayWinners] = Field(default=None)
    """Optional. A giveaway with public winners was completed"""
    giveaway_completed: Optional[GiveawayCompleted] = Field(default=None)
    """Optional. Service message: a giveaway without public winners was completed"""
    managed_bot_created: Optional[ManagedBotCreated] = Field(default=None)
    """Optional. Service message: user created a bot that will be managed by the current bot"""
    paid_message_price_changed: Optional[PaidMessagePriceChanged] = Field(default=None)
    """Optional. Service message: the price for paid messages has changed in the chat"""
    poll_option_added: Optional[PollOptionAdded] = Field(default=None)
    """Optional. Service message: answer option was added to a poll"""
    poll_option_deleted: Optional[PollOptionDeleted] = Field(default=None)
    """Optional. Service message: answer option was deleted from a poll"""
    suggested_post_approved: Optional[SuggestedPostApproved] = Field(default=None)
    """Optional. Service message: a suggested post was approved"""
    suggested_post_approval_failed: Optional[SuggestedPostApprovalFailed] = Field(default=None)
    """Optional. Service message: approval of a suggested post has failed"""
    suggested_post_declined: Optional[SuggestedPostDeclined] = Field(default=None)
    """Optional. Service message: a suggested post was declined"""
    suggested_post_paid: Optional[SuggestedPostPaid] = Field(default=None)
    """Optional. Service message: payment for a suggested post was received"""
    suggested_post_refunded: Optional[SuggestedPostRefunded] = Field(default=None)
    """Optional. Service message: payment for a suggested post was refunded"""
    video_chat_scheduled: Optional[VideoChatScheduled] = Field(default=None)
    """Optional. Service message: video chat scheduled"""
    video_chat_started: Optional[VideoChatStarted] = Field(default=None)
    """Optional. Service message: video chat started"""
    video_chat_ended: Optional[VideoChatEnded] = Field(default=None)
    """Optional. Service message: video chat ended"""
    video_chat_participants_invited: Optional[VideoChatParticipantsInvited] = Field(default=None)
    """Optional. Service message: new participants invited to a video chat"""
    web_app_data: Optional[WebAppData] = Field(default=None)
    """Optional. Service message: data sent by a Web App"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message. login_url buttons are represented as ordinary url buttons."""

    async def answer(
        self,
        text: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_message(), но чат — чат этого сообщения.
        
        Use this method to send text messages. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendmessage
        """
        return await self._require_bot().send_message(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply(
        self,
        text: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_message(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send text messages. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendmessage
        """
        return await self._require_bot().send_message(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def forward(
        self,
        chat_id: Union[int, str],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        video_start_timestamp: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
    ) -> Message:
        """Как bot.forward_message(), но источник — это сообщение, чат назначения задаёте вы.
        
        Use this method to forward messages of any kind. Service messages and messages with protected content can't be forwarded. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#forwardmessage
        """
        return await self._require_bot().forward_message(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            from_chat_id=self.chat.id,
            video_start_timestamp=video_start_timestamp,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            message_id=self.message_id,
        )

    async def copy_to(
        self,
        chat_id: Union[int, str],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        video_start_timestamp: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> MessageId:
        """Как bot.copy_message(), но источник — это сообщение, чат назначения задаёте вы.
        
        Use this method to copy messages of any kind. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_ids is known to the bot. The method is analogous to the method forwardMessage, but the copied message doesn't have a link to the original message. Returns the MessageId of the sent message on success.
        
        https://core.telegram.org/bots/api#copymessage
        """
        return await self._require_bot().copy_message(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            from_chat_id=self.chat.id,
            message_id=self.message_id,
            video_start_timestamp=video_start_timestamp,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_photo(
        self,
        photo: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_photo(), но чат — чат этого сообщения.
        
        Use this method to send photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendphoto
        """
        return await self._require_bot().send_photo(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_photo(
        self,
        photo: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_photo(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendphoto
        """
        return await self._require_bot().send_photo(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_live_photo(
        self,
        live_photo: Union[InputFile, str],
        photo: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_live_photo(), но чат — чат этого сообщения.
        
        Use this method to send live photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlivephoto
        """
        return await self._require_bot().send_live_photo(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            live_photo=live_photo,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_live_photo(
        self,
        live_photo: Union[InputFile, str],
        photo: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_live_photo(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send live photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlivephoto
        """
        return await self._require_bot().send_live_photo(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            live_photo=live_photo,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_audio(
        self,
        audio: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_audio(), но чат — чат этого сообщения.
        
        Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .MP3 or .M4A format. On success, the sent Message is returned. Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.
        
        For sending voice messages, use the sendVoice method instead.
        
        https://core.telegram.org/bots/api#sendaudio
        """
        return await self._require_bot().send_audio(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_audio(
        self,
        audio: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_audio(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .MP3 or .M4A format. On success, the sent Message is returned. Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.
        
        For sending voice messages, use the sendVoice method instead.
        
        https://core.telegram.org/bots/api#sendaudio
        """
        return await self._require_bot().send_audio(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_document(
        self,
        document: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_document(), но чат — чат этого сообщения.
        
        Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#senddocument
        """
        return await self._require_bot().send_document(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            document=document,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_document(
        self,
        document: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_document(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#senddocument
        """
        return await self._require_bot().send_document(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            document=document,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_video(
        self,
        video: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        cover: Optional[Union[InputFile, str]] = None,
        start_timestamp: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_video(), но чат — чат этого сообщения.
        
        Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvideo
        """
        return await self._require_bot().send_video(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            video=video,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            cover=cover,
            start_timestamp=start_timestamp,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_video(
        self,
        video: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        cover: Optional[Union[InputFile, str]] = None,
        start_timestamp: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_video(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvideo
        """
        return await self._require_bot().send_video(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            video=video,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            cover=cover,
            start_timestamp=start_timestamp,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_animation(
        self,
        animation: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_animation(), но чат — чат этого сообщения.
        
        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendanimation
        """
        return await self._require_bot().send_animation(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            animation=animation,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_animation(
        self,
        animation: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_animation(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendanimation
        """
        return await self._require_bot().send_animation(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            animation=animation,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_voice(
        self,
        voice: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_voice(), но чат — чат этого сообщения.
        
        Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other formats may be sent as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvoice
        """
        return await self._require_bot().send_voice(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_voice(
        self,
        voice: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_voice(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other formats may be sent as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvoice
        """
        return await self._require_bot().send_voice(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_video_note(
        self,
        video_note: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_video_note(), но чат — чат этого сообщения.
        
        Use this method to send a rounded square MPEG4 video of up to 1 minute long. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvideonote
        """
        return await self._require_bot().send_video_note(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            video_note=video_note,
            duration=duration,
            length=length,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_video_note(
        self,
        video_note: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_video_note(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send a rounded square MPEG4 video of up to 1 minute long. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvideonote
        """
        return await self._require_bot().send_video_note(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            video_note=video_note,
            duration=duration,
            length=length,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_paid_media(
        self,
        star_count: int,
        media: List[InputPaidMedia],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        payload: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_paid_media(), но чат — чат этого сообщения.
        
        Use this method to send paid media. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpaidmedia
        """
        return await self._require_bot().send_paid_media(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            star_count=star_count,
            media=media,
            payload=payload,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_paid_media(
        self,
        star_count: int,
        media: List[InputPaidMedia],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        payload: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_paid_media(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send paid media. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpaidmedia
        """
        return await self._require_bot().send_paid_media(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            star_count=star_count,
            media=media,
            payload=payload,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_media_group(
        self,
        media: Union[List[InputMediaAudio], List[InputMediaDocument], List[InputMediaLivePhoto], List[InputMediaPhoto], List[InputMediaVideo]],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
    ) -> List[Message]:
        """Как bot.send_media_group(), но чат — чат этого сообщения.
        
        Use this method to send a group of photos, live photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an Array of Message objects that were sent is returned.
        
        https://core.telegram.org/bots/api#sendmediagroup
        """
        return await self._require_bot().send_media_group(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
        )

    async def reply_media_group(
        self,
        media: Union[List[InputMediaAudio], List[InputMediaDocument], List[InputMediaLivePhoto], List[InputMediaPhoto], List[InputMediaVideo]],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
    ) -> List[Message]:
        """Как bot.send_media_group(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send a group of photos, live photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an Array of Message objects that were sent is returned.
        
        https://core.telegram.org/bots/api#sendmediagroup
        """
        return await self._require_bot().send_media_group(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
        )

    async def answer_location(
        self,
        latitude: float,
        longitude: float,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_location(), но чат — чат этого сообщения.
        
        Use this method to send point on the map. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlocation
        """
        return await self._require_bot().send_location(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_location(
        self,
        latitude: float,
        longitude: float,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_location(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send point on the map. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlocation
        """
        return await self._require_bot().send_location(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_venue(), но чат — чат этого сообщения.
        
        Use this method to send information about a venue. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvenue
        """
        return await self._require_bot().send_venue(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_venue(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send information about a venue. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvenue
        """
        return await self._require_bot().send_venue(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_contact(
        self,
        phone_number: str,
        first_name: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_contact(), но чат — чат этого сообщения.
        
        Use this method to send phone contacts. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendcontact
        """
        return await self._require_bot().send_contact(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_contact(
        self,
        phone_number: str,
        first_name: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_contact(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send phone contacts. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendcontact
        """
        return await self._require_bot().send_contact(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_poll(
        self,
        question: str,
        options: List[InputPollOption],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        question_parse_mode: Optional[str] = None,
        question_entities: Optional[List[MessageEntity]] = None,
        is_anonymous: Optional[bool] = None,
        type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        allows_revoting: Optional[bool] = None,
        shuffle_options: Optional[bool] = None,
        allow_adding_options: Optional[bool] = None,
        hide_results_until_closes: Optional[bool] = None,
        members_only: Optional[bool] = None,
        country_codes: Optional[List[str]] = None,
        correct_option_ids: Optional[List[int]] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[str] = None,
        explanation_entities: Optional[List[MessageEntity]] = None,
        explanation_media: Optional[InputPollMedia] = None,
        open_period: Optional[int] = None,
        close_date: Optional[int] = None,
        is_closed: Optional[bool] = None,
        description: Optional[str] = None,
        description_parse_mode: Optional[str] = None,
        description_entities: Optional[List[MessageEntity]] = None,
        media: Optional[InputPollMedia] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_poll(), но чат — чат этого сообщения.
        
        Use this method to send a native poll. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpoll
        """
        return await self._require_bot().send_poll(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            question=question,
            question_parse_mode=question_parse_mode,
            question_entities=question_entities,
            options=options,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            allows_revoting=allows_revoting,
            shuffle_options=shuffle_options,
            allow_adding_options=allow_adding_options,
            hide_results_until_closes=hide_results_until_closes,
            members_only=members_only,
            country_codes=country_codes,
            correct_option_ids=correct_option_ids,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            explanation_media=explanation_media,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            description=description,
            description_parse_mode=description_parse_mode,
            description_entities=description_entities,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_poll(
        self,
        question: str,
        options: List[InputPollOption],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        question_parse_mode: Optional[str] = None,
        question_entities: Optional[List[MessageEntity]] = None,
        is_anonymous: Optional[bool] = None,
        type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        allows_revoting: Optional[bool] = None,
        shuffle_options: Optional[bool] = None,
        allow_adding_options: Optional[bool] = None,
        hide_results_until_closes: Optional[bool] = None,
        members_only: Optional[bool] = None,
        country_codes: Optional[List[str]] = None,
        correct_option_ids: Optional[List[int]] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[str] = None,
        explanation_entities: Optional[List[MessageEntity]] = None,
        explanation_media: Optional[InputPollMedia] = None,
        open_period: Optional[int] = None,
        close_date: Optional[int] = None,
        is_closed: Optional[bool] = None,
        description: Optional[str] = None,
        description_parse_mode: Optional[str] = None,
        description_entities: Optional[List[MessageEntity]] = None,
        media: Optional[InputPollMedia] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_poll(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send a native poll. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpoll
        """
        return await self._require_bot().send_poll(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            question=question,
            question_parse_mode=question_parse_mode,
            question_entities=question_entities,
            options=options,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            allows_revoting=allows_revoting,
            shuffle_options=shuffle_options,
            allow_adding_options=allow_adding_options,
            hide_results_until_closes=hide_results_until_closes,
            members_only=members_only,
            country_codes=country_codes,
            correct_option_ids=correct_option_ids,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            explanation_media=explanation_media,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            description=description,
            description_parse_mode=description_parse_mode,
            description_entities=description_entities,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_checklist(
        self,
        business_connection_id: str,
        checklist: InputChecklist,
        *,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_checklist(), но чат — чат этого сообщения.
        
        Use this method to send a checklist on behalf of a connected business account. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendchecklist
        """
        return await self._require_bot().send_checklist(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            checklist=checklist,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_checklist(
        self,
        business_connection_id: str,
        checklist: InputChecklist,
        *,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_checklist(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send a checklist on behalf of a connected business account. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendchecklist
        """
        return await self._require_bot().send_checklist(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            checklist=checklist,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_dice(
        self,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_dice(), но чат — чат этого сообщения.
        
        Use this method to send an animated emoji that will display a random value. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#senddice
        """
        return await self._require_bot().send_dice(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_dice(
        self,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_dice(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send an animated emoji that will display a random value. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#senddice
        """
        return await self._require_bot().send_dice(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_message_draft(
        self,
        draft_id: int,
        *,
        message_thread_id: Optional[int] = None,
        text: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        can_stop: Optional[bool] = None,
        keep_on_stop: Optional[bool] = None,
    ) -> bool:
        """Как bot.send_message_draft(), но чат — чат этого сообщения.
        
        Use this method to stream a partial message to a user while the message is being generated. Note that the streamed draft is ephemeral and acts as a temporary 30-second preview - once the output is finalized, you must call sendMessage with the complete message to persist it in the user's chat. Returns True on success.
        
        https://core.telegram.org/bots/api#sendmessagedraft
        """
        return await self._require_bot().send_message_draft(
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            draft_id=draft_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            can_stop=can_stop,
            keep_on_stop=keep_on_stop,
        )

    async def answer_chat_action(
        self,
        action: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> bool:
        """Как bot.send_chat_action(), но чат — чат этого сообщения.
        
        Use this method when you need to tell the user that something is happening on the bot's side. The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status). Returns True on success.
        
        We only recommend using this method when a response from the bot will take a noticeable amount of time to arrive.
        
        https://core.telegram.org/bots/api#sendchataction
        """
        return await self._require_bot().send_chat_action(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            action=action,
        )

    async def set_reaction(
        self,
        *,
        reaction: Optional[List[ReactionType]] = None,
        is_big: Optional[bool] = None,
    ) -> bool:
        """Как bot.set_message_reaction(), но правит это сообщение.
        
        Use this method to change the chosen reactions on a message. Service messages of some types can't be reacted to. Automatically forwarded messages from a channel to its discussion group have the same available reactions as messages in the channel. Bots can't use paid reactions. Returns True on success.
        
        https://core.telegram.org/bots/api#setmessagereaction
        """
        return await self._require_bot().set_message_reaction(
            chat_id=self.chat.id,
            message_id=self.message_id,
            reaction=reaction,
            is_big=is_big,
        )

    async def pin(
        self,
        *,
        business_connection_id: Optional[str] = None,
        disable_notification: Optional[bool] = None,
    ) -> bool:
        """Как bot.pin_chat_message(), но правит это сообщение.
        
        Use this method to add a message to the list of pinned messages in a chat. In private chats and channel direct messages chats, all non-service messages can be pinned. Conversely, the bot must be an administrator with the 'can_pin_messages' right or the 'can_edit_messages' right to pin messages in groups and channels respectively. Returns True on success.
        
        https://core.telegram.org/bots/api#pinchatmessage
        """
        return await self._require_bot().pin_chat_message(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
            disable_notification=disable_notification,
        )

    async def unpin(
        self,
        *,
        business_connection_id: Optional[str] = None,
    ) -> bool:
        """Как bot.unpin_chat_message(), но правит это сообщение.
        
        Use this method to remove a message from the list of pinned messages in a chat. In private chats and channel direct messages chats, all messages can be unpinned. Conversely, the bot must be an administrator with the 'can_pin_messages' right or the 'can_edit_messages' right to unpin messages in groups and channels respectively. Returns True on success.
        
        https://core.telegram.org/bots/api#unpinchatmessage
        """
        return await self._require_bot().unpin_chat_message(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
        )

    async def read(
        self,
        business_connection_id: str,
    ) -> bool:
        """Как bot.read_business_message(), но правит это сообщение.
        
        Marks incoming message as read on behalf of a business account. Requires the can_read_messages business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#readbusinessmessage
        """
        return await self._require_bot().read_business_message(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
        )

    async def edit_text(
        self,
        text: Optional[str] = None,
        *,
        business_connection_id: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        rich_message: Optional[InputRichMessage] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.edit_message_text(), но правит это сообщение.
        
        Use this method to edit text, rich and game messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
        https://core.telegram.org/bots/api#editmessagetext
        """
        return await self._require_bot().edit_message_text(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            rich_message=rich_message,
            reply_markup=reply_markup,
        )

    async def edit_caption(
        self,
        caption: Optional[str] = None,
        *,
        business_connection_id: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.edit_message_caption(), но правит это сообщение.
        
        Use this method to edit captions of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
        https://core.telegram.org/bots/api#editmessagecaption
        """
        return await self._require_bot().edit_message_caption(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            reply_markup=reply_markup,
        )

    async def edit_media(
        self,
        media: InputMedia,
        *,
        business_connection_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.edit_message_media(), но правит это сообщение.
        
        Use this method to edit animation, audio, document, live photo, photo, or video messages, or to replace a text or a rich message with a media. If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo, a live photo, or a video otherwise. When an inline message is edited, a new file can't be uploaded; use a previously uploaded file via its file_id or specify a URL. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
        https://core.telegram.org/bots/api#editmessagemedia
        """
        return await self._require_bot().edit_message_media(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
            media=media,
            reply_markup=reply_markup,
        )

    async def edit_live_location(
        self,
        latitude: float,
        longitude: float,
        *,
        business_connection_id: Optional[str] = None,
        live_period: Optional[int] = None,
        horizontal_accuracy: Optional[float] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.edit_message_live_location(), но правит это сообщение.
        
        Use this method to edit live location messages. A location can be edited until its live_period expires or editing is explicitly disabled by a call to stopMessageLiveLocation. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.
        
        https://core.telegram.org/bots/api#editmessagelivelocation
        """
        return await self._require_bot().edit_message_live_location(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
            latitude=latitude,
            longitude=longitude,
            live_period=live_period,
            horizontal_accuracy=horizontal_accuracy,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            reply_markup=reply_markup,
        )

    async def stop_live_location(
        self,
        *,
        business_connection_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.stop_message_live_location(), но правит это сообщение.
        
        Use this method to stop updating a live location message before live_period expires. On success, if the message is not an inline message, the edited Message is returned, otherwise True is returned.
        
        https://core.telegram.org/bots/api#stopmessagelivelocation
        """
        return await self._require_bot().stop_message_live_location(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
            reply_markup=reply_markup,
        )

    async def edit_checklist(
        self,
        business_connection_id: str,
        checklist: InputChecklist,
        *,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.edit_message_checklist(), но правит это сообщение.
        
        Use this method to edit a checklist on behalf of a connected business account. On success, the edited Message is returned.
        
        https://core.telegram.org/bots/api#editmessagechecklist
        """
        return await self._require_bot().edit_message_checklist(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
            checklist=checklist,
            reply_markup=reply_markup,
        )

    async def edit_reply_markup(
        self,
        *,
        business_connection_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.edit_message_reply_markup(), но правит это сообщение.
        
        Use this method to edit only the reply markup of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
        https://core.telegram.org/bots/api#editmessagereplymarkup
        """
        return await self._require_bot().edit_message_reply_markup(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
            reply_markup=reply_markup,
        )

    async def stop_poll(
        self,
        *,
        business_connection_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Poll:
        """Как bot.stop_poll(), но правит это сообщение.
        
        Use this method to stop a poll which was sent by the bot. On success, the stopped Poll is returned.
        
        https://core.telegram.org/bots/api#stoppoll
        """
        return await self._require_bot().stop_poll(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
            reply_markup=reply_markup,
        )

    async def approve_suggested_post(
        self,
        *,
        send_date: Optional[int] = None,
    ) -> bool:
        """Как bot.approve_suggested_post(), но правит это сообщение.
        
        Use this method to approve a suggested post in a direct messages chat. The bot must have the 'can_post_messages' administrator right in the corresponding channel chat. Returns True on success.
        
        https://core.telegram.org/bots/api#approvesuggestedpost
        """
        return await self._require_bot().approve_suggested_post(
            chat_id=self.chat.id,
            message_id=self.message_id,
            send_date=send_date,
        )

    async def decline_suggested_post(
        self,
        *,
        comment: Optional[str] = None,
    ) -> bool:
        """Как bot.decline_suggested_post(), но правит это сообщение.
        
        Use this method to decline a suggested post in a direct messages chat. The bot must have the 'can_manage_direct_messages' administrator right in the corresponding channel chat. Returns True on success.
        
        https://core.telegram.org/bots/api#declinesuggestedpost
        """
        return await self._require_bot().decline_suggested_post(
            chat_id=self.chat.id,
            message_id=self.message_id,
            comment=comment,
        )

    async def delete(
        self,
    ) -> bool:
        """Как bot.delete_message(), но правит это сообщение.
        
        Use this method to delete a message, including service messages, with the following limitations:
        
        - A message can only be deleted if it was sent less than 48 hours ago.
        
        - Service messages about a supergroup, channel, or forum topic creation can't be deleted.
        
        - A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.
        
        - Bots can delete outgoing messages in private chats, groups, and supergroups.
        
        - Bots can delete incoming messages in private chats.
        
        - Bots granted can_post_messages permissions can delete outgoing messages in channels.
        
        - If the bot is an administrator of a group, it can delete any message there.
        
        - If the bot has can_delete_messages administrator right in a supergroup or a channel, it can delete any message there.
        
        - If the bot has can_manage_direct_messages administrator right in a channel, it can delete any message in the corresponding direct messages chat.
        
        Returns True on success.
        
        https://core.telegram.org/bots/api#deletemessage
        """
        return await self._require_bot().delete_message(
            chat_id=self.chat.id,
            message_id=self.message_id,
        )

    async def delete_reaction(
        self,
        *,
        user_id: Optional[int] = None,
        actor_chat_id: Optional[int] = None,
    ) -> bool:
        """Как bot.delete_message_reaction(), но правит это сообщение.
        
        Use this method to remove a reaction from a message in a group or a supergroup chat. The bot must have the 'can_delete_messages' administrator right in the chat. Returns True on success.
        
        https://core.telegram.org/bots/api#deletemessagereaction
        """
        return await self._require_bot().delete_message_reaction(
            chat_id=self.chat.id,
            message_id=self.message_id,
            user_id=user_id,
            actor_chat_id=actor_chat_id,
        )

    async def answer_sticker(
        self,
        sticker: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_sticker(), но чат — чат этого сообщения.
        
        Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendsticker
        """
        return await self._require_bot().send_sticker(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            sticker=sticker,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_sticker(
        self,
        sticker: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_sticker(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendsticker
        """
        return await self._require_bot().send_sticker(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            sticker=sticker,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_rich_message(
        self,
        rich_message: InputRichMessage,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_rich_message(), но чат — чат этого сообщения.
        
        Use this method to send rich messages. If the message contains a block with a media element, then the bot must have the right to send the media to the chat. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendrichmessage
        """
        return await self._require_bot().send_rich_message(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            rich_message=rich_message,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_rich_message(
        self,
        rich_message: InputRichMessage,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_rich_message(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send rich messages. If the message contains a block with a media element, then the bot must have the right to send the media to the chat. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendrichmessage
        """
        return await self._require_bot().send_rich_message(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            rich_message=rich_message,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_rich_message_draft(
        self,
        draft_id: int,
        rich_message: InputRichMessage,
        *,
        message_thread_id: Optional[int] = None,
        can_stop: Optional[bool] = None,
        keep_on_stop: Optional[bool] = None,
    ) -> bool:
        """Как bot.send_rich_message_draft(), но чат — чат этого сообщения.
        
        Use this method to stream a partial rich message to a user while the message is being generated. Note that the streamed draft is ephemeral and acts as a temporary 30-second preview - once the output is finalized, you must call sendRichMessage with the complete message to persist it in the user's chat. Returns True on success.
        
        https://core.telegram.org/bots/api#sendrichmessagedraft
        """
        return await self._require_bot().send_rich_message_draft(
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            draft_id=draft_id,
            rich_message=rich_message,
            can_stop=can_stop,
            keep_on_stop=keep_on_stop,
        )

    async def answer_invoice(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: List[LabeledPrice],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        provider_token: Optional[str] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
        start_parameter: Optional[str] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_invoice(), но чат — чат этого сообщения.
        
        Use this method to send invoices. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendinvoice
        """
        return await self._require_bot().send_invoice(
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            start_parameter=start_parameter,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_invoice(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: List[LabeledPrice],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        provider_token: Optional[str] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
        start_parameter: Optional[str] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_invoice(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send invoices. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendinvoice
        """
        return await self._require_bot().send_invoice(
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            direct_messages_topic_id=direct_messages_topic_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            start_parameter=start_parameter,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def answer_game(
        self,
        game_short_name: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_game(), но чат — чат этого сообщения.
        
        Use this method to send a game. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendgame
        """
        return await self._require_bot().send_game(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_game(
        self,
        game_short_name: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_game(), но чат — чат этого сообщения, цитирует его.
        
        Use this method to send a game. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendgame
        """
        return await self._require_bot().send_game(
            business_connection_id=business_connection_id if business_connection_id is not None else self.business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id if message_thread_id is not None else (self.message_thread_id if self.is_topic_message else None),
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters if reply_parameters is not None else ReplyParameters(message_id=self.message_id),
            reply_markup=reply_markup,
        )

    async def set_game_score(
        self,
        user_id: int,
        score: int,
        *,
        force: Optional[bool] = None,
        disable_edit_message: Optional[bool] = None,
    ) -> Union[Message, bool]:
        """Как bot.set_game_score(), но правит это сообщение.
        
        Use this method to set the score of the specified user in a game message. On success, if the message is not an inline message, the Message is returned, otherwise True is returned. Returns an error, if the new score is not greater than the user's current score in the chat and force is False.
        
        https://core.telegram.org/bots/api#setgamescore
        """
        return await self._require_bot().set_game_score(
            user_id=user_id,
            score=score,
            force=force,
            disable_edit_message=disable_edit_message,
            chat_id=self.chat.id,
            message_id=self.message_id,
        )

    async def get_game_high_scores(
        self,
        user_id: int,
    ) -> List[GameHighScore]:
        """Как bot.get_game_high_scores(), но правит это сообщение.
        
        Use this method to get data for high score tables. Will return the score of the specified user and several of their neighbors in a game. Returns an Array of GameHighScore objects.
        
        https://core.telegram.org/bots/api#getgamehighscores
        """
        return await self._require_bot().get_game_high_scores(
            user_id=user_id,
            chat_id=self.chat.id,
            message_id=self.message_id,
        )

class MessageId(_Base, frozen=True):
    """This object represents a unique message identifier.
    
    https://core.telegram.org/bots/api#messageid
    """
    message_id: int
    """Unique message identifier. In specific instances (e.g., message containing a video sent to a big chat), the server might automatically schedule a message instead of sending it immediately. In such cases, this field will be 0 and the relevant message will be unusable until it is actually sent."""

class InaccessibleMessage(_Base, frozen=True):
    """This object describes a message that was deleted or is otherwise inaccessible to the bot.
    
    https://core.telegram.org/bots/api#inaccessiblemessage
    """
    chat: Chat
    """Chat the message belonged to"""
    message_id: int
    """Unique message identifier inside the chat"""
    date: int
    """Always 0. The field can be used to differentiate regular and inaccessible messages."""

class MessageEntity(_Base, frozen=True):
    """This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.
    
    https://core.telegram.org/bots/api#messageentity
    """
    type: str
    """Type of the entity. Currently, can be "mention" (@username), "hashtag" (#hashtag or #hashtag@chatusername), "cashtag" ($USD or $USD@chatusername), "bot_command" (/start@jobs_bot), "url" (https://telegram.org), "email" (do-not-reply@telegram.org), "phone_number" (+1-212-555-0123), "bold" (bold text), "italic" (italic text), "underline" (underlined text), "strikethrough" (strikethrough text), "spoiler" (spoiler message), "blockquote" (block quotation), "expandable_blockquote" (collapsed-by-default block quotation), "code" (monowidth string), "pre" (monowidth block), "text_link" (for clickable text URLs), "text_mention" (for users without usernames), "custom_emoji" (for inline custom emoji stickers), or "date_time" (for formatted date and time)."""
    offset: int
    """Offset in UTF-16 code units to the start of the entity"""
    length: int
    """Length of the entity in UTF-16 code units"""
    url: Optional[str] = Field(default=None)
    """Optional. For "text_link" only, URL that will be opened after user taps on the text"""
    user: Optional[User] = Field(default=None)
    """Optional. For "text_mention" only, the mentioned user"""
    language: Optional[str] = Field(default=None)
    """Optional. For "pre" only, the programming language of the entity text"""
    custom_emoji_id: Optional[str] = Field(default=None)
    """Optional. For "custom_emoji" only, unique identifier of the custom emoji. Use getCustomEmojiStickers to get full information about the sticker."""
    unix_time: Optional[int] = Field(default=None)
    """Optional. For "date_time" only, the Unix time associated with the entity"""
    date_time_format: Optional[str] = Field(default=None)
    """Optional. For "date_time" only, the string that defines the formatting of the date and time. See date-time entity formatting for more details."""

class TextQuote(_Base, frozen=True):
    """This object contains information about the quoted part of a message that is replied to by the given message.
    
    https://core.telegram.org/bots/api#textquote
    """
    text: str
    """Text of the quoted part of a message that is replied to by the given message"""
    entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities that appear in the quote. Currently, only bold, italic, underline, strikethrough, spoiler, custom_emoji, and date_time entities are kept in quotes."""
    position: int
    """Approximate quote position in the original message in UTF-16 code units as specified by the sender"""
    is_manual: Optional[bool] = Field(default=None)
    """Optional. True, if the quote was chosen manually by the message sender. Otherwise, the quote was added automatically by the server."""

class ExternalReplyInfo(_Base, frozen=True):
    """This object contains information about a message that is being replied to, which may come from another chat or forum topic.
    
    https://core.telegram.org/bots/api#externalreplyinfo
    """
    origin: MessageOrigin
    """Origin of the message replied to by the given message"""
    chat: Optional[Chat] = Field(default=None)
    """Optional. Chat the original message belongs to. Available only if the chat is a supergroup or a channel."""
    message_id: Optional[int] = Field(default=None)
    """Optional. Unique message identifier inside the original chat. Available only if the original chat is a supergroup or a channel."""
    link_preview_options: Optional[LinkPreviewOptions] = Field(default=None)
    """Optional. Options used for link preview generation for the original message, if it is a text message"""
    animation: Optional[Animation] = Field(default=None)
    """Optional. Message is an animation, information about the animation"""
    audio: Optional[Audio] = Field(default=None)
    """Optional. Message is an audio file, information about the file"""
    document: Optional[Document] = Field(default=None)
    """Optional. Message is a general file, information about the file"""
    live_photo: Optional[LivePhoto] = Field(default=None)
    """Optional. Message is a live photo, information about the live photo"""
    paid_media: Optional[PaidMediaInfo] = Field(default=None)
    """Optional. Message contains paid media; information about the paid media"""
    photo: Optional[List[PhotoSize]] = Field(default=None)
    """Optional. Message is a photo, available sizes of the photo"""
    sticker: Optional[Sticker] = Field(default=None)
    """Optional. Message is a sticker, information about the sticker"""
    story: Optional[Story] = Field(default=None)
    """Optional. Message is a forwarded story"""
    video: Optional[Video] = Field(default=None)
    """Optional. Message is a video, information about the video"""
    video_note: Optional[VideoNote] = Field(default=None)
    """Optional. Message is a video note, information about the video message"""
    voice: Optional[Voice] = Field(default=None)
    """Optional. Message is a voice message, information about the file"""
    has_media_spoiler: Optional[bool] = Field(default=None)
    """Optional. True, if the message media is covered by a spoiler animation"""
    checklist: Optional[Checklist] = Field(default=None)
    """Optional. Message is a checklist"""
    contact: Optional[Contact] = Field(default=None)
    """Optional. Message is a shared contact, information about the contact"""
    dice: Optional[Dice] = Field(default=None)
    """Optional. Message is a dice with random value"""
    game: Optional[Game] = Field(default=None)
    """Optional. Message is a game, information about the game. More about games: https://core.telegram.org/bots/api#games"""
    giveaway: Optional[Giveaway] = Field(default=None)
    """Optional. Message is a scheduled giveaway, information about the giveaway"""
    giveaway_winners: Optional[GiveawayWinners] = Field(default=None)
    """Optional. A giveaway with public winners was completed"""
    invoice: Optional[Invoice] = Field(default=None)
    """Optional. Message is an invoice for a payment, information about the invoice. More about payments: https://core.telegram.org/bots/api#payments"""
    location: Optional[Location] = Field(default=None)
    """Optional. Message is a shared location, information about the location"""
    poll: Optional[Poll] = Field(default=None)
    """Optional. Message is a native poll, information about the poll"""
    venue: Optional[Venue] = Field(default=None)
    """Optional. Message is a venue, information about the venue"""

class ReplyParameters(_Base, frozen=True):
    """Describes reply parameters for the message that is being sent.
    
    https://core.telegram.org/bots/api#replyparameters
    """
    message_id: Optional[int] = Field(default=None)
    """Optional. Identifier of the message that will be replied to in the current chat, or in the chat chat_id if it is specified. Required if ephemeral_message_id isn't specified."""
    chat_id: Optional[Union[int, str]] = Field(default=None)
    """Optional. If the message to be replied to is from a different chat, unique identifier for the chat or username of the bot, supergroup or channel in the format @username. Not supported for messages sent on behalf of a business account, messages from channel direct messages chats and ephemeral messages."""
    ephemeral_message_id: Optional[int] = Field(default=None)
    """Optional. Identifier of the incoming ephemeral message that will be replied to in the current chat. A reply to an ephemeral message must itself be an ephemeral message. An ephemeral message may only be replied to within 15 seconds of being sent. Required if message_id isn't specified."""
    allow_sending_without_reply: Optional[bool] = Field(default=None)
    """Optional. Pass True if the message should be sent even if the specified message to be replied to is not found. Always False for replies in another chat or forum topic, and sent ephemeral messages. Always True for messages sent on behalf of a business account."""
    quote: Optional[str] = Field(default=None)
    """Optional. Quoted part of the message to be replied to; 0-1024 characters after entities parsing. The quote must be an exact substring of the message to be replied to, including bold, italic, underline, strikethrough, spoiler, custom_emoji, and date_time entities. The message will fail to send if the quote isn't found in the original message. Ignored for ephemeral messages."""
    quote_parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the quote. See formatting options for more details."""
    quote_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. A JSON-serialized list of special entities that appear in the quote. It can be specified instead of quote_parse_mode."""
    quote_position: Optional[int] = Field(default=None)
    """Optional. Position of the quote in the original message in UTF-16 code units"""
    checklist_task_id: Optional[int] = Field(default=None)
    """Optional. Identifier of the specific checklist task to be replied to"""
    poll_option_id: Optional[str] = Field(default=None)
    """Optional. Persistent identifier of the specific poll option to be replied to"""

class EphemeralMessageParameters(_Base, frozen=True):
    """https://core.telegram.org/bots/api#ephemeralmessageparameters"""
    receiver_user_id: int
    """Identifier of the user who will receive the message. It is not guaranteed that the user will receive the message, especially if they are offline. See here for more details."""
    callback_query_id: Optional[str] = Field(default=None)
    """Optional. Identifier of the callback query which triggered the message, if any"""
    replace_callback_query_message: Optional[bool] = Field(default=None)
    """Optional. Pass True if the ephemeral message must be shown in place of the original message. Must be False for callback queries from ephemeral messages, which must be edited using regular editEphemeralMessage... methods."""

class MessageOriginUser(_Base, frozen=True):
    """The message was originally sent by a known user.
    
    https://core.telegram.org/bots/api#messageoriginuser
    """
    type: Literal["user"] = Field(default='user')
    """Type of the message origin, always "user" """
    date: int
    """Date the message was sent originally in Unix time"""
    sender_user: User
    """User that sent the message originally"""

class MessageOriginHiddenUser(_Base, frozen=True):
    """The message was originally sent by an unknown user.
    
    https://core.telegram.org/bots/api#messageoriginhiddenuser
    """
    type: Literal["hidden_user"] = Field(default='hidden_user')
    """Type of the message origin, always "hidden_user" """
    date: int
    """Date the message was sent originally in Unix time"""
    sender_user_name: str
    """Name of the user that sent the message originally"""

class MessageOriginChat(_Base, frozen=True):
    """The message was originally sent on behalf of a chat to a group chat.
    
    https://core.telegram.org/bots/api#messageoriginchat
    """
    type: Literal["chat"] = Field(default='chat')
    """Type of the message origin, always "chat" """
    date: int
    """Date the message was sent originally in Unix time"""
    sender_chat: Chat
    """Chat that sent the message originally"""
    author_signature: Optional[str] = Field(default=None)
    """Optional. For messages originally sent by an anonymous chat administrator, original message author signature"""

class MessageOriginChannel(_Base, frozen=True):
    """The message was originally sent to a channel chat.
    
    https://core.telegram.org/bots/api#messageoriginchannel
    """
    type: Literal["channel"] = Field(default='channel')
    """Type of the message origin, always "channel" """
    date: int
    """Date the message was sent originally in Unix time"""
    chat: Chat
    """Channel chat to which the message was originally sent"""
    message_id: int
    """Unique message identifier inside the chat"""
    author_signature: Optional[str] = Field(default=None)
    """Optional. Signature of the original post author"""

class PhotoSize(_Base, frozen=True):
    """This object represents one size of a photo or a file / sticker thumbnail.
    
    https://core.telegram.org/bots/api#photosize
    """
    file_id: str
    """Identifier for this file, which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    width: int
    """Photo width"""
    height: int
    """Photo height"""
    file_size: Optional[int] = Field(default=None)
    """Optional. File size in bytes"""

class Animation(_Base, frozen=True):
    """This object represents an animation file (GIF or H.264/MPEG-4 AVC video without sound).
    
    https://core.telegram.org/bots/api#animation
    """
    file_id: str
    """Identifier for this file, which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    width: int
    """Video width as defined by the sender"""
    height: int
    """Video height as defined by the sender"""
    duration: int
    """Duration of the video in seconds as defined by the sender"""
    thumbnail: Optional[PhotoSize] = Field(default=None)
    """Optional. Animation thumbnail as defined by the sender"""
    file_name: Optional[str] = Field(default=None)
    """Optional. Original animation filename as defined by the sender"""
    mime_type: Optional[str] = Field(default=None)
    """Optional. MIME type of the file as defined by the sender"""
    file_size: Optional[int] = Field(default=None)
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value."""

class Audio(_Base, frozen=True):
    """This object represents an audio file to be treated as music by the Telegram clients.
    
    https://core.telegram.org/bots/api#audio
    """
    file_id: str
    """Identifier for this file, which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    duration: int
    """Duration of the audio in seconds as defined by the sender"""
    performer: Optional[str] = Field(default=None)
    """Optional. Performer of the audio as defined by the sender or by audio tags"""
    title: Optional[str] = Field(default=None)
    """Optional. Title of the audio as defined by the sender or by audio tags"""
    file_name: Optional[str] = Field(default=None)
    """Optional. Original filename as defined by the sender"""
    mime_type: Optional[str] = Field(default=None)
    """Optional. MIME type of the file as defined by the sender"""
    file_size: Optional[int] = Field(default=None)
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value."""
    thumbnail: Optional[PhotoSize] = Field(default=None)
    """Optional. Thumbnail of the album cover to which the music file belongs"""

class Document(_Base, frozen=True):
    """This object represents a general file (as opposed to photos, voice messages and audio files).
    
    https://core.telegram.org/bots/api#document
    """
    file_id: str
    """Identifier for this file, which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    thumbnail: Optional[PhotoSize] = Field(default=None)
    """Optional. Document thumbnail as defined by the sender"""
    file_name: Optional[str] = Field(default=None)
    """Optional. Original filename as defined by the sender"""
    mime_type: Optional[str] = Field(default=None)
    """Optional. MIME type of the file as defined by the sender"""
    file_size: Optional[int] = Field(default=None)
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value."""

class LivePhoto(_Base, frozen=True):
    """This object represents a live photo.
    
    https://core.telegram.org/bots/api#livephoto
    """
    photo: Optional[List[PhotoSize]] = Field(default=None)
    """Optional. Available sizes of the corresponding static photo"""
    file_id: str
    """Identifier for the video file which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for the video file which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    width: int
    """Video width as defined by the sender"""
    height: int
    """Video height as defined by the sender"""
    duration: int
    """Duration of the video in seconds as defined by the sender"""
    mime_type: Optional[str] = Field(default=None)
    """Optional. MIME type of the file as defined by the sender"""
    file_size: Optional[int] = Field(default=None)
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value."""

class Story(_Base, frozen=True):
    """This object represents a story.
    
    https://core.telegram.org/bots/api#story
    """
    chat: Chat
    """Chat that posted the story"""
    id: int
    """Unique identifier for the story in the chat"""

class VideoQuality(_Base, frozen=True):
    """This object represents a video file of a specific quality.
    
    https://core.telegram.org/bots/api#videoquality
    """
    file_id: str
    """Identifier for this file, which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    width: int
    """Video width"""
    height: int
    """Video height"""
    codec: str
    """Codec that was used to encode the video, for example, "h264", "h265", or "av01" """
    file_size: Optional[int] = Field(default=None)
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value."""

class Video(_Base, frozen=True):
    """This object represents a video file.
    
    https://core.telegram.org/bots/api#video
    """
    file_id: str
    """Identifier for this file, which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    width: int
    """Video width as defined by the sender"""
    height: int
    """Video height as defined by the sender"""
    duration: int
    """Duration of the video in seconds as defined by the sender"""
    thumbnail: Optional[PhotoSize] = Field(default=None)
    """Optional. Video thumbnail"""
    cover: Optional[List[PhotoSize]] = Field(default=None)
    """Optional. Available sizes of the cover of the video in the message"""
    start_timestamp: Optional[int] = Field(default=None)
    """Optional. Timestamp in seconds from which the video will play in the message"""
    qualities: Optional[List[VideoQuality]] = Field(default=None)
    """Optional. List of available qualities of the video"""
    file_name: Optional[str] = Field(default=None)
    """Optional. Original filename as defined by the sender"""
    mime_type: Optional[str] = Field(default=None)
    """Optional. MIME type of the file as defined by the sender"""
    file_size: Optional[int] = Field(default=None)
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value."""

class VideoNote(_Base, frozen=True):
    """This object represents a video message.
    
    https://core.telegram.org/bots/api#videonote
    """
    file_id: str
    """Identifier for this file, which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    length: int
    """Video width and height (diameter of the video message) as defined by the sender"""
    duration: int
    """Duration of the video in seconds as defined by the sender"""
    thumbnail: Optional[PhotoSize] = Field(default=None)
    """Optional. Video thumbnail"""
    file_size: Optional[int] = Field(default=None)
    """Optional. File size in bytes"""

class Voice(_Base, frozen=True):
    """This object represents a voice note.
    
    https://core.telegram.org/bots/api#voice
    """
    file_id: str
    """Identifier for this file, which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    duration: int
    """Duration of the audio in seconds as defined by the sender"""
    mime_type: Optional[str] = Field(default=None)
    """Optional. MIME type of the file as defined by the sender"""
    file_size: Optional[int] = Field(default=None)
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value."""

class PaidMediaInfo(_Base, frozen=True):
    """Describes the paid media added to a message.
    
    https://core.telegram.org/bots/api#paidmediainfo
    """
    star_count: int
    """The number of Telegram Stars that must be paid to buy access to the media"""
    paid_media: List[PaidMedia]
    """Information about the paid media"""

class PaidMediaLivePhoto(_Base, frozen=True):
    """The paid media is a live photo.
    
    https://core.telegram.org/bots/api#paidmedialivephoto
    """
    type: Literal["live_photo"] = Field(default='live_photo')
    """Type of the paid media, always "live_photo" """
    live_photo: LivePhoto
    """The photo"""

class PaidMediaPhoto(_Base, frozen=True):
    """The paid media is a photo.
    
    https://core.telegram.org/bots/api#paidmediaphoto
    """
    type: Literal["photo"] = Field(default='photo')
    """Type of the paid media, always "photo" """
    photo: List[PhotoSize]
    """The photo"""

class PaidMediaPreview(_Base, frozen=True):
    """The paid media isn't available before the payment.
    
    https://core.telegram.org/bots/api#paidmediapreview
    """
    type: Literal["preview"] = Field(default='preview')
    """Type of the paid media, always "preview" """
    width: Optional[int] = Field(default=None)
    """Optional. Media width as defined by the sender"""
    height: Optional[int] = Field(default=None)
    """Optional. Media height as defined by the sender"""
    duration: Optional[int] = Field(default=None)
    """Optional. Duration of the media in seconds as defined by the sender"""

class PaidMediaVideo(_Base, frozen=True):
    """The paid media is a video.
    
    https://core.telegram.org/bots/api#paidmediavideo
    """
    type: Literal["video"] = Field(default='video')
    """Type of the paid media, always "video" """
    video: Video
    """The video"""

class Contact(_Base, frozen=True):
    """This object represents a phone contact.
    
    https://core.telegram.org/bots/api#contact
    """
    phone_number: str
    """Contact's phone number"""
    first_name: str
    """Contact's first name"""
    last_name: Optional[str] = Field(default=None)
    """Optional. Contact's last name"""
    user_id: Optional[int] = Field(default=None)
    """Optional. Contact's user identifier in Telegram. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier."""
    vcard: Optional[str] = Field(default=None)
    """Optional. Additional data about the contact in the form of a vCard"""

class Dice(_Base, frozen=True):
    """This object represents an animated emoji that displays a random value.
    
    https://core.telegram.org/bots/api#dice
    """
    emoji: str
    """Emoji on which the dice throw animation is based"""
    value: int
    """Value of the dice, 1-6 for "🎲", "🎯" and "🎳" base emoji, 1-5 for "🏀" and "⚽" base emoji, 1-64 for "🎰" base emoji"""

class Link(_Base, frozen=True):
    """Represents an HTTP link.
    
    https://core.telegram.org/bots/api#link
    """
    url: str
    """URL of the link"""

class PollMedia(_Base, frozen=True):
    """At most one of the optional fields can be present in any given object.
    
    https://core.telegram.org/bots/api#pollmedia
    """
    animation: Optional[Animation] = Field(default=None)
    """Optional. Media is an animation, information about the animation"""
    audio: Optional[Audio] = Field(default=None)
    """Optional. Media is an audio file, information about the file; currently, can't be received in a poll option"""
    document: Optional[Document] = Field(default=None)
    """Optional. Media is a general file, information about the file; currently, can't be received in a poll option"""
    link: Optional[Link] = Field(default=None)
    """Optional. The HTTP link attached to the poll option"""
    live_photo: Optional[LivePhoto] = Field(default=None)
    """Optional. Media is a live photo, information about the live photo"""
    location: Optional[Location] = Field(default=None)
    """Optional. Media is a shared location, information about the location"""
    photo: Optional[List[PhotoSize]] = Field(default=None)
    """Optional. Media is a photo, available sizes of the photo"""
    sticker: Optional[Sticker] = Field(default=None)
    """Optional. Media is a sticker, information about the sticker; currently, for poll options only"""
    venue: Optional[Venue] = Field(default=None)
    """Optional. Media is a venue, information about the venue"""
    video: Optional[Video] = Field(default=None)
    """Optional. Media is a video, information about the video"""

class PollOption(_Base, frozen=True):
    """This object contains information about one answer option in a poll.
    
    https://core.telegram.org/bots/api#polloption
    """
    persistent_id: str
    """Unique identifier of the option, persistent on option addition and deletion"""
    text: str
    """Option text, 1-100 characters"""
    text_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities that appear in the option text. Currently, only custom emoji entities are allowed in poll option texts"""
    media: Optional[PollMedia] = Field(default=None)
    """Optional. Media added to the poll option"""
    voter_count: int
    """Number of users who voted for this option; may be 0 if unknown"""
    added_by_user: Optional[User] = Field(default=None)
    """Optional. User who added the option; omitted if the option wasn't added by a user after poll creation"""
    added_by_chat: Optional[Chat] = Field(default=None)
    """Optional. Chat that added the option; omitted if the option wasn't added by a chat after poll creation"""
    addition_date: Optional[int] = Field(default=None)
    """Optional. Point in time (Unix timestamp) when the option was added; omitted if the option existed in the original poll"""

class InputPollOption(_Base, frozen=True):
    """This object contains information about one answer option in a poll to be sent.
    
    https://core.telegram.org/bots/api#inputpolloption
    """
    text: str
    """Option text, 1-100 characters"""
    text_parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the text. See formatting options for more details. Currently, only custom emoji entities are allowed."""
    text_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. A JSON-serialized list of special entities that appear in the poll option text. It can be specified instead of text_parse_mode."""
    media: Optional[InputPollOptionMedia] = Field(default=None)
    """Optional. Media added to the poll option"""

class PollAnswer(_Base, frozen=True):
    """This object represents an answer of a user in a non-anonymous poll.
    
    https://core.telegram.org/bots/api#pollanswer
    """
    poll_id: str
    """Unique poll identifier"""
    voter_chat: Optional[Chat] = Field(default=None)
    """Optional. The chat that changed the answer to the poll, if the voter is anonymous"""
    user: Optional[User] = Field(default=None)
    """Optional. The user that changed the answer to the poll, if the voter isn't anonymous"""
    option_ids: List[int]
    """0-based identifiers of chosen answer options. May be empty if the vote was retracted."""
    option_persistent_ids: List[str]
    """Persistent identifiers of the chosen answer options. May be empty if the vote was retracted."""

class Poll(_Base, frozen=True):
    """This object contains information about a poll.
    
    https://core.telegram.org/bots/api#poll
    """
    id: str
    """Unique poll identifier"""
    question: str
    """Poll question, 1-300 characters"""
    question_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities that appear in the question. Currently, only custom emoji entities are allowed in poll questions"""
    options: List[PollOption]
    """List of poll options"""
    total_voter_count: int
    """Total number of users that voted in the poll"""
    is_closed: bool
    """True, if the poll is closed"""
    is_anonymous: bool
    """True, if the poll is anonymous"""
    type: str
    """Poll type, currently can be "regular" or "quiz" """
    allows_multiple_answers: bool
    """True, if the poll allows multiple answers"""
    allows_revoting: bool
    """True, if the poll allows to change the chosen answer options"""
    members_only: bool
    """True if voting is limited to users who have been members of the chat where the poll was originally sent for more than 24 hours"""
    country_codes: Optional[List[str]] = Field(default=None)
    """Optional. A list of two-letter ISO 3166-1 alpha-2 country codes indicating the countries from which users can vote in the poll. The country code "FT" is used for users with anonymous numbers. If omitted, then users from any country can participate in the poll."""
    correct_option_ids: Optional[List[int]] = Field(default=None)
    """Optional. Array of 0-based identifiers of the correct answer options. Available only for polls in quiz mode which are closed or were sent (not forwarded) by the bot or to the private chat with the bot."""
    explanation: Optional[str] = Field(default=None)
    """Optional. Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters"""
    explanation_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities like usernames, URLs, bot commands, etc. that appear in the explanation"""
    explanation_media: Optional[PollMedia] = Field(default=None)
    """Optional. Media added to the quiz explanation"""
    open_period: Optional[int] = Field(default=None)
    """Optional. Amount of time in seconds the poll will be active after creation"""
    close_date: Optional[int] = Field(default=None)
    """Optional. Point in time (Unix timestamp) when the poll will be automatically closed"""
    description: Optional[str] = Field(default=None)
    """Optional. Description of the poll; for polls inside the Message object only"""
    description_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities like usernames, URLs, bot commands, etc. that appear in the description"""
    media: Optional[PollMedia] = Field(default=None)
    """Optional. Media added to the poll description; for polls inside the Message object only"""

class ChecklistTask(_Base, frozen=True):
    """Describes a task in a checklist.
    
    https://core.telegram.org/bots/api#checklisttask
    """
    id: int
    """Unique identifier of the task"""
    text: str
    """Text of the task"""
    text_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities that appear in the task text"""
    completed_by_user: Optional[User] = Field(default=None)
    """Optional. User that completed the task; omitted if the task wasn't completed by a user"""
    completed_by_chat: Optional[Chat] = Field(default=None)
    """Optional. Chat that completed the task; omitted if the task wasn't completed by a chat"""
    completion_date: Optional[int] = Field(default=None)
    """Optional. Point in time (Unix timestamp) when the task was completed; 0 if the task wasn't completed"""

class Checklist(_Base, frozen=True):
    """Describes a checklist.
    
    https://core.telegram.org/bots/api#checklist
    """
    title: str
    """Title of the checklist"""
    title_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities that appear in the checklist title"""
    tasks: List[ChecklistTask]
    """List of tasks in the checklist"""
    others_can_add_tasks: Optional[bool] = Field(default=None)
    """Optional. True, if users other than the creator of the list can add tasks to the list"""
    others_can_mark_tasks_as_done: Optional[bool] = Field(default=None)
    """Optional. True, if users other than the creator of the list can mark tasks as done or not done"""

class InputChecklistTask(_Base, frozen=True):
    """Describes a task to add to a checklist.
    
    https://core.telegram.org/bots/api#inputchecklisttask
    """
    id: int
    """Unique identifier of the task; must be positive and unique among all task identifiers currently present in the checklist"""
    text: str
    """Text of the task; 1-100 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the text. See formatting options for more details."""
    text_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the text, which can be specified instead of parse_mode. Currently, only bold, italic, underline, strikethrough, spoiler, custom_emoji, and date_time entities are allowed."""

class InputChecklist(_Base, frozen=True):
    """Describes a checklist to create.
    
    https://core.telegram.org/bots/api#inputchecklist
    """
    title: str
    """Title of the checklist; 1-255 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the title. See formatting options for more details."""
    title_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the title, which can be specified instead of parse_mode. Currently, only bold, italic, underline, strikethrough, spoiler, custom_emoji, and date_time entities are allowed."""
    tasks: List[InputChecklistTask]
    """List of 1-30 tasks in the checklist"""
    others_can_add_tasks: Optional[bool] = Field(default=None)
    """Optional. Pass True if other users can add tasks to the checklist"""
    others_can_mark_tasks_as_done: Optional[bool] = Field(default=None)
    """Optional. Pass True if other users can mark tasks as done or not done in the checklist"""

class Location(_Base, frozen=True):
    """This object represents a point on the map.
    
    https://core.telegram.org/bots/api#location
    """
    latitude: float
    """Latitude as defined by the sender"""
    longitude: float
    """Longitude as defined by the sender"""
    horizontal_accuracy: Optional[float] = Field(default=None)
    """Optional. The radius of uncertainty for the location, measured in meters; 0-1500"""
    live_period: Optional[int] = Field(default=None)
    """Optional. Time relative to the message sending date, during which the location can be updated; in seconds. For active live locations only."""
    heading: Optional[int] = Field(default=None)
    """Optional. The direction in which user is moving, in degrees; 1-360. For active live locations only."""
    proximity_alert_radius: Optional[int] = Field(default=None)
    """Optional. The maximum distance for proximity alerts about approaching another chat member, in meters. For sent live locations only."""

class Venue(_Base, frozen=True):
    """This object represents a venue.
    
    https://core.telegram.org/bots/api#venue
    """
    location: Location
    """Venue location. Can't be a live location."""
    title: str
    """Name of the venue"""
    address: str
    """Address of the venue"""
    foursquare_id: Optional[str] = Field(default=None)
    """Optional. Foursquare identifier of the venue"""
    foursquare_type: Optional[str] = Field(default=None)
    """Optional. Foursquare type of the venue. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)"""
    google_place_id: Optional[str] = Field(default=None)
    """Optional. Google Places identifier of the venue"""
    google_place_type: Optional[str] = Field(default=None)
    """Optional. Google Places type of the venue. (See supported types.)"""

class WebAppData(_Base, frozen=True):
    """Describes data sent from a Web App to the bot.
    
    https://core.telegram.org/bots/api#webappdata
    """
    data: str
    """The data. Be aware that a bad client can send arbitrary data in this field."""
    button_text: str
    """Text of the web_app keyboard button from which the Web App was opened. Be aware that a bad client can send arbitrary data in this field."""

class ProximityAlertTriggered(_Base, frozen=True):
    """This object represents the content of a service message, sent whenever a user in the chat triggers a proximity alert set by another user.
    
    https://core.telegram.org/bots/api#proximityalerttriggered
    """
    traveler: User
    """User that triggered the alert"""
    watcher: User
    """User that set the alert"""
    distance: int
    """The distance between the users"""

class MessageAutoDeleteTimerChanged(_Base, frozen=True):
    """This object represents a service message about a change in auto-delete timer settings.
    
    https://core.telegram.org/bots/api#messageautodeletetimerchanged
    """
    message_auto_delete_time: int
    """New auto-delete time for messages in the chat; in seconds"""

class ManagedBotCreated(_Base, frozen=True):
    """This object contains information about the bot that was created to be managed by the current bot.
    
    https://core.telegram.org/bots/api#managedbotcreated
    """
    bot: User
    """Information about the bot. The bot's token can be fetched using the method getManagedBotToken."""

class ManagedBotUpdated(_Base, frozen=True):
    """This object contains information about the creation, token update, or owner update of a bot that is managed by the current bot.
    
    https://core.telegram.org/bots/api#managedbotupdated
    """
    user: User
    """User that created the bot"""
    bot: User
    """Information about the bot. Token of the bot can be fetched using the method getManagedBotToken."""

class BotSubscriptionUpdated(_Base, frozen=True):
    """This object contains information about changes to a user payment subscription toward the current bot.
    
    https://core.telegram.org/bots/api#botsubscriptionupdated
    """
    user: User
    """User who subscribed for payments toward the bot"""
    invoice_payload: str
    """Bot-specified invoice payload"""
    state: str
    """The new state of the subscription. Currently, it can be one of "canceled" if the user canceled the subscription, "active" if the user re-enabled a previously canceled subscription, or "failed" if payment for the subscription failed."""

class MessageGenerationStopped(_Base, frozen=True):
    """This object describes an update about a user stopping message generation.
    
    https://core.telegram.org/bots/api#messagegenerationstopped
    """
    chat: Chat
    """Chat in which the message is generated"""
    message_thread_id: Optional[int] = Field(default=None)
    """Optional. Unique identifier of the message thread in which the message is generated"""
    draft_id: int
    """Unique identifier of the message draft which was stopped"""

class PollOptionAdded(_Base, frozen=True):
    """Describes a service message about an option added to a poll.
    
    https://core.telegram.org/bots/api#polloptionadded
    """
    poll_message: Optional[MaybeInaccessibleMessage] = Field(default=None)
    """Optional. Message containing the poll to which the option was added, if known. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    option_persistent_id: str
    """Unique identifier of the added option"""
    option_text: str
    """Option text"""
    option_text_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities that appear in the option_text"""

class PollOptionDeleted(_Base, frozen=True):
    """Describes a service message about an option deleted from a poll.
    
    https://core.telegram.org/bots/api#polloptiondeleted
    """
    poll_message: Optional[MaybeInaccessibleMessage] = Field(default=None)
    """Optional. Message containing the poll from which the option was deleted, if known. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    option_persistent_id: str
    """Unique identifier of the deleted option"""
    option_text: str
    """Option text"""
    option_text_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities that appear in the option_text"""

class ChatBoostAdded(_Base, frozen=True):
    """This object represents a service message about a user boosting a chat.
    
    https://core.telegram.org/bots/api#chatboostadded
    """
    boost_count: int
    """Number of boosts added by the user"""

class BackgroundFillSolid(_Base, frozen=True):
    """The background is filled using the selected color.
    
    https://core.telegram.org/bots/api#backgroundfillsolid
    """
    type: Literal["solid"] = Field(default='solid')
    """Type of the background fill, always "solid" """
    color: int
    """The color of the background fill in the RGB24 format"""

class BackgroundFillGradient(_Base, frozen=True):
    """The background is a gradient fill.
    
    https://core.telegram.org/bots/api#backgroundfillgradient
    """
    type: Literal["gradient"] = Field(default='gradient')
    """Type of the background fill, always "gradient" """
    top_color: int
    """Top color of the gradient in the RGB24 format"""
    bottom_color: int
    """Bottom color of the gradient in the RGB24 format"""
    rotation_angle: int
    """Clockwise rotation angle of the background fill in degrees; 0-359"""

class BackgroundFillFreeformGradient(_Base, frozen=True):
    """The background is a freeform gradient that rotates after every message in the chat.
    
    https://core.telegram.org/bots/api#backgroundfillfreeformgradient
    """
    type: Literal["freeform_gradient"] = Field(default='freeform_gradient')
    """Type of the background fill, always "freeform_gradient" """
    colors: List[int]
    """A list of the 3 or 4 base colors that are used to generate the freeform gradient in the RGB24 format"""

class BackgroundTypeFill(_Base, frozen=True):
    """The background is automatically filled based on the selected colors.
    
    https://core.telegram.org/bots/api#backgroundtypefill
    """
    type: Literal["fill"] = Field(default='fill')
    """Type of the background, always "fill" """
    fill: BackgroundFill
    """The background fill"""
    dark_theme_dimming: int
    """Dimming of the background in dark themes, as a percentage; 0-100"""

class BackgroundTypeWallpaper(_Base, frozen=True):
    """The background is a wallpaper in the JPEG format.
    
    https://core.telegram.org/bots/api#backgroundtypewallpaper
    """
    type: Literal["wallpaper"] = Field(default='wallpaper')
    """Type of the background, always "wallpaper" """
    document: Document
    """Document with the wallpaper"""
    dark_theme_dimming: int
    """Dimming of the background in dark themes, as a percentage; 0-100"""
    is_blurred: Optional[bool] = Field(default=None)
    """Optional. True, if the wallpaper is downscaled to fit in a 450x450 square and then box-blurred with radius 12"""
    is_moving: Optional[bool] = Field(default=None)
    """Optional. True, if the background moves slightly when the device is tilted"""

class BackgroundTypePattern(_Base, frozen=True):
    """The background is a .PNG or .TGV (gzipped subset of SVG with MIME type "application/x-tgwallpattern") pattern to be combined with the background fill chosen by the user.
    
    https://core.telegram.org/bots/api#backgroundtypepattern
    """
    type: Literal["pattern"] = Field(default='pattern')
    """Type of the background, always "pattern" """
    document: Document
    """Document with the pattern"""
    fill: BackgroundFill
    """The background fill that is combined with the pattern"""
    intensity: int
    """Intensity of the pattern when it is shown above the filled background; 0-100"""
    is_inverted: Optional[bool] = Field(default=None)
    """Optional. True, if the background fill must be applied only to the pattern itself. All other pixels are black in this case. For dark themes only."""
    is_moving: Optional[bool] = Field(default=None)
    """Optional. True, if the background moves slightly when the device is tilted"""

class BackgroundTypeChatTheme(_Base, frozen=True):
    """The background is taken directly from a built-in chat theme.
    
    https://core.telegram.org/bots/api#backgroundtypechattheme
    """
    type: Literal["chat_theme"] = Field(default='chat_theme')
    """Type of the background, always "chat_theme" """
    theme_name: str
    """Name of the chat theme, which is usually an emoji"""

class ChatBackground(_Base, frozen=True):
    """This object represents a chat background.
    
    https://core.telegram.org/bots/api#chatbackground
    """
    type: BackgroundType
    """Type of the background"""

class ChecklistTasksDone(_Base, frozen=True):
    """Describes a service message about checklist tasks marked as done or not done.
    
    https://core.telegram.org/bots/api#checklisttasksdone
    """
    checklist_message: Optional[Message] = Field(default=None)
    """Optional. Message containing the checklist whose tasks were marked as done or not done. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    marked_as_done_task_ids: Optional[List[int]] = Field(default=None)
    """Optional. Identifiers of the tasks that were marked as done"""
    marked_as_not_done_task_ids: Optional[List[int]] = Field(default=None)
    """Optional. Identifiers of the tasks that were marked as not done"""

class ChecklistTasksAdded(_Base, frozen=True):
    """Describes a service message about tasks added to a checklist.
    
    https://core.telegram.org/bots/api#checklisttasksadded
    """
    checklist_message: Optional[Message] = Field(default=None)
    """Optional. Message containing the checklist to which the tasks were added. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    tasks: List[ChecklistTask]
    """List of tasks added to the checklist"""

class CommunityChatAdded(_Base, frozen=True):
    """Describes a service message about a chat or a bot being added to a community.
    
    https://core.telegram.org/bots/api#communitychatadded
    """
    community: Community
    """The new community to which the chat or the bot belongs"""

class CommunityChatJoined(_Base, frozen=True):
    """Describes a service message about a chat being joined by a user from a community.
    
    https://core.telegram.org/bots/api#communitychatjoined
    """
    community: Community
    """The community from which the chat was joined"""

class CommunityChatRemoved(_Base, frozen=True):
    """Describes a service message about a chat or a bot being removed from a community. Currently holds no information.
    
    https://core.telegram.org/bots/api#communitychatremoved
    """

class ForumTopicCreated(_Base, frozen=True):
    """This object represents a service message about a new forum topic created in the chat.
    
    https://core.telegram.org/bots/api#forumtopiccreated
    """
    name: str
    """Name of the topic"""
    icon_color: int
    """Color of the topic icon in RGB format"""
    icon_custom_emoji_id: Optional[str] = Field(default=None)
    """Optional. Unique identifier of the custom emoji shown as the topic icon"""
    is_name_implicit: Optional[bool] = Field(default=None)
    """Optional. True, if the name of the topic wasn't specified explicitly by its creator and likely needs to be changed by the bot"""

class ForumTopicClosed(_Base, frozen=True):
    """This object represents a service message about a forum topic closed in the chat. Currently holds no information.
    
    https://core.telegram.org/bots/api#forumtopicclosed
    """

class ForumTopicEdited(_Base, frozen=True):
    """This object represents a service message about an edited forum topic.
    
    https://core.telegram.org/bots/api#forumtopicedited
    """
    name: Optional[str] = Field(default=None)
    """Optional. New name of the topic, if it was edited"""
    icon_custom_emoji_id: Optional[str] = Field(default=None)
    """Optional. New identifier of the custom emoji shown as the topic icon, if it was edited; an empty string if the icon was removed"""

class ForumTopicReopened(_Base, frozen=True):
    """This object represents a service message about a forum topic reopened in the chat. Currently holds no information.
    
    https://core.telegram.org/bots/api#forumtopicreopened
    """

class GeneralForumTopicHidden(_Base, frozen=True):
    """This object represents a service message about General forum topic hidden in the chat. Currently holds no information.
    
    https://core.telegram.org/bots/api#generalforumtopichidden
    """

class GeneralForumTopicUnhidden(_Base, frozen=True):
    """This object represents a service message about General forum topic unhidden in the chat. Currently holds no information.
    
    https://core.telegram.org/bots/api#generalforumtopicunhidden
    """

class SharedUser(_Base, frozen=True):
    """This object contains information about a user that was shared with the bot using a KeyboardButtonRequestUsers button.
    
    https://core.telegram.org/bots/api#shareduser
    """
    user_id: int
    """Identifier of the shared user. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so 64-bit integers or double-precision float types are safe for storing these identifiers. The bot may not have access to the user and could be unable to use this identifier, unless the user is already known to the bot by some other means."""
    first_name: Optional[str] = Field(default=None)
    """Optional. First name of the user, if the name was requested by the bot"""
    last_name: Optional[str] = Field(default=None)
    """Optional. Last name of the user, if the name was requested by the bot"""
    username: Optional[str] = Field(default=None)
    """Optional. Username of the user, if the username was requested by the bot"""
    photo: Optional[List[PhotoSize]] = Field(default=None)
    """Optional. Available sizes of the chat photo, if the photo was requested by the bot"""

class UsersShared(_Base, frozen=True):
    """This object contains information about the users whose identifiers were shared with the bot using a KeyboardButtonRequestUsers button.
    
    https://core.telegram.org/bots/api#usersshared
    """
    request_id: int
    """Identifier of the request"""
    users: List[SharedUser]
    """Information about users shared with the bot"""

class ChatShared(_Base, frozen=True):
    """This object contains information about a chat that was shared with the bot using a KeyboardButtonRequestChat button.
    
    https://core.telegram.org/bots/api#chatshared
    """
    request_id: int
    """Identifier of the request"""
    chat_id: int
    """Identifier of the shared chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier. The bot may not have access to the chat and could be unable to use this identifier, unless the chat is already known to the bot by some other means."""
    title: Optional[str] = Field(default=None)
    """Optional. Title of the chat, if the title was requested by the bot"""
    username: Optional[str] = Field(default=None)
    """Optional. Username of the chat, if the username was requested by the bot and available"""
    photo: Optional[List[PhotoSize]] = Field(default=None)
    """Optional. Available sizes of the chat photo, if the photo was requested by the bot"""

class WriteAccessAllowed(_Base, frozen=True):
    """This object represents a service message about a user allowing a bot to write messages after adding it to the attachment menu, launching a Web App from a link, or accepting an explicit request from a Web App sent by the method requestWriteAccess.
    
    https://core.telegram.org/bots/api#writeaccessallowed
    """
    from_request: Optional[bool] = Field(default=None)
    """Optional. True, if the access was granted after the user accepted an explicit request from a Web App sent by the method requestWriteAccess"""
    web_app_name: Optional[str] = Field(default=None)
    """Optional. Name of the Web App, if the access was granted when the Web App was launched from a link"""
    from_attachment_menu: Optional[bool] = Field(default=None)
    """Optional. True, if the access was granted when the bot was added to the attachment or side menu"""

class VideoChatScheduled(_Base, frozen=True):
    """This object represents a service message about a video chat scheduled in the chat.
    
    https://core.telegram.org/bots/api#videochatscheduled
    """
    start_date: int
    """Point in time (Unix timestamp) when the video chat is supposed to be started by a chat administrator"""

class VideoChatStarted(_Base, frozen=True):
    """This object represents a service message about a video chat started in the chat. Currently holds no information.
    
    https://core.telegram.org/bots/api#videochatstarted
    """

class VideoChatEnded(_Base, frozen=True):
    """This object represents a service message about a video chat ended in the chat.
    
    https://core.telegram.org/bots/api#videochatended
    """
    duration: int
    """Video chat duration in seconds"""

class VideoChatParticipantsInvited(_Base, frozen=True):
    """This object represents a service message about new members invited to a video chat.
    
    https://core.telegram.org/bots/api#videochatparticipantsinvited
    """
    users: List[User]
    """New members that were invited to the video chat"""

class PaidMessagePriceChanged(_Base, frozen=True):
    """Describes a service message about a change in the price of paid messages within a chat.
    
    https://core.telegram.org/bots/api#paidmessagepricechanged
    """
    paid_message_star_count: int
    """The new number of Telegram Stars that must be paid by non-administrator users of the supergroup chat for each sent message"""

class DirectMessagePriceChanged(_Base, frozen=True):
    """Describes a service message about a change in the price of direct messages sent to a channel chat.
    
    https://core.telegram.org/bots/api#directmessagepricechanged
    """
    are_direct_messages_enabled: bool
    """True, if direct messages are enabled for the channel chat; False otherwise"""
    direct_message_star_count: Optional[int] = Field(default=None)
    """Optional. The new number of Telegram Stars that must be paid by users for each direct message sent to the channel. Does not apply to users who have been exempted by administrators. Defaults to 0."""

class SuggestedPostApproved(_Base, frozen=True):
    """Describes a service message about the approval of a suggested post.
    
    https://core.telegram.org/bots/api#suggestedpostapproved
    """
    suggested_post_message: Optional[Message] = Field(default=None)
    """Optional. Message containing the suggested post. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    price: Optional[SuggestedPostPrice] = Field(default=None)
    """Optional. Amount paid for the post"""
    send_date: int
    """Date when the post will be published"""

class SuggestedPostApprovalFailed(_Base, frozen=True):
    """Describes a service message about the failed approval of a suggested post. Currently, only caused by insufficient user funds at the time of approval.
    
    https://core.telegram.org/bots/api#suggestedpostapprovalfailed
    """
    suggested_post_message: Optional[Message] = Field(default=None)
    """Optional. Message containing the suggested post whose approval has failed. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    price: SuggestedPostPrice
    """Expected price of the post"""

class SuggestedPostDeclined(_Base, frozen=True):
    """Describes a service message about the rejection of a suggested post.
    
    https://core.telegram.org/bots/api#suggestedpostdeclined
    """
    suggested_post_message: Optional[Message] = Field(default=None)
    """Optional. Message containing the suggested post. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    comment: Optional[str] = Field(default=None)
    """Optional. Comment with which the post was declined"""

class SuggestedPostPaid(_Base, frozen=True):
    """Describes a service message about a successful payment for a suggested post.
    
    https://core.telegram.org/bots/api#suggestedpostpaid
    """
    suggested_post_message: Optional[Message] = Field(default=None)
    """Optional. Message containing the suggested post. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    currency: str
    """Currency in which the payment was made. Currently, one of "XTR" for Telegram Stars or "TON" for TON grams."""
    amount: Optional[int] = Field(default=None)
    """Optional. The amount of the currency that was received by the channel in nanograms; for payments in TON grams only"""
    star_amount: Optional[StarAmount] = Field(default=None)
    """Optional. The amount of Telegram Stars that was received by the channel; for payments in Telegram Stars only"""

class SuggestedPostRefunded(_Base, frozen=True):
    """Describes a service message about a payment refund for a suggested post.
    
    https://core.telegram.org/bots/api#suggestedpostrefunded
    """
    suggested_post_message: Optional[Message] = Field(default=None)
    """Optional. Message containing the suggested post. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    reason: str
    """Reason for the refund. Currently, one of "post_deleted" if the post was deleted within 24 hours of being posted or removed from scheduled messages without being posted, or "payment_refunded" if the payer refunded their payment."""

class GiveawayCreated(_Base, frozen=True):
    """This object represents a service message about the creation of a scheduled giveaway.
    
    https://core.telegram.org/bots/api#giveawaycreated
    """
    prize_star_count: Optional[int] = Field(default=None)
    """Optional. The number of Telegram Stars to be split between giveaway winners; for Telegram Star giveaways only"""

class Giveaway(_Base, frozen=True):
    """This object represents a message about a scheduled giveaway.
    
    https://core.telegram.org/bots/api#giveaway
    """
    chats: List[Chat]
    """The list of chats which the user must join to participate in the giveaway"""
    winners_selection_date: int
    """Point in time (Unix timestamp) when winners of the giveaway will be selected"""
    winner_count: int
    """The number of users which are supposed to be selected as winners of the giveaway"""
    only_new_members: Optional[bool] = Field(default=None)
    """Optional. True, if only users who join the chats after the giveaway started should be eligible to win"""
    has_public_winners: Optional[bool] = Field(default=None)
    """Optional. True, if the list of giveaway winners will be visible to everyone"""
    prize_description: Optional[str] = Field(default=None)
    """Optional. Description of additional giveaway prize"""
    country_codes: Optional[List[str]] = Field(default=None)
    """Optional. A list of two-letter ISO 3166-1 alpha-2 country codes indicating the countries from which eligible users for the giveaway must come. If empty, then all users can participate in the giveaway. Users with a phone number that was bought on Fragment can always participate in giveaways."""
    prize_star_count: Optional[int] = Field(default=None)
    """Optional. The number of Telegram Stars to be split between giveaway winners; for Telegram Star giveaways only"""
    premium_subscription_month_count: Optional[int] = Field(default=None)
    """Optional. The number of months the Telegram Premium subscription won from the giveaway will be active for; for Telegram Premium giveaways only"""

class GiveawayWinners(_Base, frozen=True):
    """This object represents a message about the completion of a giveaway with public winners.
    
    https://core.telegram.org/bots/api#giveawaywinners
    """
    chat: Chat
    """The chat that created the giveaway"""
    giveaway_message_id: int
    """Identifier of the message with the giveaway in the chat"""
    winners_selection_date: int
    """Point in time (Unix timestamp) when winners of the giveaway were selected"""
    winner_count: int
    """Total number of winners in the giveaway"""
    winners: List[User]
    """List of up to 100 winners of the giveaway"""
    additional_chat_count: Optional[int] = Field(default=None)
    """Optional. The number of other chats the user had to join in order to be eligible for the giveaway"""
    prize_star_count: Optional[int] = Field(default=None)
    """Optional. The number of Telegram Stars that were split between giveaway winners; for Telegram Star giveaways only"""
    premium_subscription_month_count: Optional[int] = Field(default=None)
    """Optional. The number of months the Telegram Premium subscription won from the giveaway will be active for; for Telegram Premium giveaways only"""
    unclaimed_prize_count: Optional[int] = Field(default=None)
    """Optional. Number of undistributed prizes"""
    only_new_members: Optional[bool] = Field(default=None)
    """Optional. True, if only users who had joined the chats after the giveaway started were eligible to win"""
    was_refunded: Optional[bool] = Field(default=None)
    """Optional. True, if the giveaway was canceled because the payment for it was refunded"""
    prize_description: Optional[str] = Field(default=None)
    """Optional. Description of additional giveaway prize"""

class GiveawayCompleted(_Base, frozen=True):
    """This object represents a service message about the completion of a giveaway without public winners.
    
    https://core.telegram.org/bots/api#giveawaycompleted
    """
    winner_count: int
    """Number of winners in the giveaway"""
    unclaimed_prize_count: Optional[int] = Field(default=None)
    """Optional. Number of undistributed prizes"""
    giveaway_message: Optional[Message] = Field(default=None)
    """Optional. Message with the giveaway that was completed, if it wasn't deleted"""
    is_star_giveaway: Optional[bool] = Field(default=None)
    """Optional. True, if the giveaway is a Telegram Star giveaway. Otherwise, currently, the giveaway is a Telegram Premium giveaway."""

class LinkPreviewOptions(_Base, frozen=True):
    """Describes the options used for link preview generation.
    
    https://core.telegram.org/bots/api#linkpreviewoptions
    """
    is_disabled: Optional[bool] = Field(default=None)
    """Optional. True, if the link preview is disabled"""
    url: Optional[str] = Field(default=None)
    """Optional. URL to use for the link preview. If empty, then the first URL found in the message text will be used."""
    prefer_small_media: Optional[bool] = Field(default=None)
    """Optional. True, if the media in the link preview is supposed to be shrunk; ignored if the URL isn't explicitly specified or media size change isn't supported for the preview"""
    prefer_large_media: Optional[bool] = Field(default=None)
    """Optional. True, if the media in the link preview is supposed to be enlarged; ignored if the URL isn't explicitly specified or media size change isn't supported for the preview"""
    show_above_text: Optional[bool] = Field(default=None)
    """Optional. True, if the link preview must be shown above the message text; otherwise, the link preview will be shown below the message text"""

class SuggestedPostPrice(_Base, frozen=True):
    """Describes the price of a suggested post.
    
    https://core.telegram.org/bots/api#suggestedpostprice
    """
    currency: str
    """Currency in which the post will be paid. Currently, must be one of "XTR" for Telegram Stars or "TON" for TON grams."""
    amount: int
    """The amount of the currency that will be paid for the post in the smallest units of the currency, i.e. Telegram Stars or nanograms. Currently, price in Telegram Stars must be between 5 and 100000, and price in nanograms must be between 10000000 and 10000000000000."""

class SuggestedPostInfo(_Base, frozen=True):
    """Contains information about a suggested post.
    
    https://core.telegram.org/bots/api#suggestedpostinfo
    """
    state: str
    """State of the suggested post. Currently, it can be one of "pending", "approved", "declined"."""
    price: Optional[SuggestedPostPrice] = Field(default=None)
    """Optional. Proposed price of the post. If the field is omitted, then the post is unpaid."""
    send_date: Optional[int] = Field(default=None)
    """Optional. Proposed send date of the post. If the field is omitted, then the post can be published at any time within 30 days at the sole discretion of the user or administrator who approves it."""

class SuggestedPostParameters(_Base, frozen=True):
    """Contains parameters of a post that is being suggested by the bot.
    
    https://core.telegram.org/bots/api#suggestedpostparameters
    """
    price: Optional[SuggestedPostPrice] = Field(default=None)
    """Optional. Proposed price for the post. If the field is omitted, then the post is unpaid."""
    send_date: Optional[int] = Field(default=None)
    """Optional. Proposed send date of the post. If specified, then the date must be between 300 second and 2678400 seconds (30 days) in the future. If the field is omitted, then the post can be published at any time within 30 days at the sole discretion of the user who approves it."""

class DirectMessagesTopic(_Base, frozen=True):
    """Describes a topic of a direct messages chat.
    
    https://core.telegram.org/bots/api#directmessagestopic
    """
    topic_id: int
    """Unique identifier of the topic. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier."""
    user: Optional[User] = Field(default=None)
    """Optional. Information about the user that created the topic. Currently, it is always present."""

class UserProfilePhotos(_Base, frozen=True):
    """This object represent a user's profile pictures.
    
    https://core.telegram.org/bots/api#userprofilephotos
    """
    total_count: int
    """Total number of profile pictures the target user has"""
    photos: List[List[PhotoSize]]
    """Requested profile pictures (in up to 4 sizes each)"""

class UserProfileAudios(_Base, frozen=True):
    """This object represents the audios displayed on a user's profile.
    
    https://core.telegram.org/bots/api#userprofileaudios
    """
    total_count: int
    """Total number of profile audios for the target user"""
    audios: List[Audio]
    """Requested profile audios"""

class File(_Base, frozen=True):
    """This object represents a file ready to be downloaded. The file can be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile.
    
    https://core.telegram.org/bots/api#file
    """
    file_id: str
    """Identifier for this file, which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    file_size: Optional[int] = Field(default=None)
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value."""
    file_path: Optional[str] = Field(default=None)
    """Optional. File path. Use https://api.telegram.org/file/bot<token>/<file_path> to get the file."""

class WebAppInfo(_Base, frozen=True):
    """Describes a Web App.
    
    https://core.telegram.org/bots/api#webappinfo
    """
    url: str
    """An HTTPS URL of a Web App to be opened with additional data as specified in Initializing Web Apps"""

class ReplyKeyboardMarkup(_Base, frozen=True):
    """This object represents a custom keyboard with reply options (see Introduction to bots for details and examples). Not supported in channels and for messages sent on behalf of a business account.
    
    https://core.telegram.org/bots/api#replykeyboardmarkup
    """
    keyboard: List[List[KeyboardButton]]
    """Array of button rows, each represented by an Array of KeyboardButton objects"""
    is_persistent: Optional[bool] = Field(default=None)
    """Optional. Requests clients to always show the keyboard when the regular keyboard is hidden. Defaults to False, in which case the custom keyboard can be hidden and opened with a keyboard icon."""
    resize_keyboard: Optional[bool] = Field(default=None)
    """Optional. Requests clients to resize the keyboard vertically for optimal fit (e.g., make the keyboard smaller if there are just two rows of buttons). Defaults to False, in which case the custom keyboard is always of the same height as the app's standard keyboard."""
    one_time_keyboard: Optional[bool] = Field(default=None)
    """Optional. Requests clients to hide the keyboard as soon as it's been used. The keyboard will still be available, but clients will automatically display the usual letter-keyboard in the chat - the user can press a special button in the input field to see the custom keyboard again. Defaults to False."""
    input_field_placeholder: Optional[str] = Field(default=None)
    """Optional. The placeholder to be shown in the input field when the keyboard is active; 1-64 characters"""
    selective: Optional[bool] = Field(default=None)
    """Optional. Use this parameter if you want to show the keyboard to specific users only. Targets: 1) users that are @mentioned in the text of the Message object; 2) if the bot's message is a reply to a message in the same chat and forum topic, sender of the original message. Example: A user requests to change the bot's language, bot replies to the request with a keyboard to select the new language. Other users in the group don't see the keyboard."""
    force_reply: Optional[bool] = Field(default=None)
    """Optional. Pass True if the reply interface must be shown to the user, as if they had manually selected the bot's message and tapped 'Reply'"""

class KeyboardButton(_Base, frozen=True):
    """This object represents one button of the reply keyboard. At most one of the fields other than text, icon_custom_emoji_id, and style must be used to specify the type of the button. For simple text buttons, String can be used instead of this object to specify the button text.
    
    https://core.telegram.org/bots/api#keyboardbutton
    """
    text: str
    """Text of the button. If none of the fields other than text, icon_custom_emoji_id, and style are used, it will be sent as a message when the button is pressed."""
    icon_custom_emoji_id: Optional[str] = Field(default=None)
    """Optional. Unique identifier of the custom emoji shown before the text of the button. Can only be used by bots that purchased additional usernames on Fragment or in the messages directly sent by the bot to private, group and supergroup chats if the owner of the bot has a Telegram Premium subscription."""
    style: Optional[str] = Field(default=None)
    """Optional. Style of the button. Must be one of "danger" (red), "success" (green) or "primary" (blue). If omitted, then an app-specific style is used."""
    request_users: Optional[KeyboardButtonRequestUsers] = Field(default=None)
    """Optional. If specified, pressing the button will open a list of suitable users. Identifiers of selected users will be sent to the bot in a "users_shared" service message. Available in private chats only."""
    request_chat: Optional[KeyboardButtonRequestChat] = Field(default=None)
    """Optional. If specified, pressing the button will open a list of suitable chats. Tapping on a chat will send its identifier to the bot in a "chat_shared" service message. Available in private chats only."""
    request_managed_bot: Optional[KeyboardButtonRequestManagedBot] = Field(default=None)
    """Optional. If specified, pressing the button will ask the user to create and share a bot that will be managed by the current bot. Available for bots that enabled management of other bots in the @BotFather Mini App. Available in private chats only."""
    request_contact: Optional[bool] = Field(default=None)
    """Optional. If True, the user's phone number will be sent as a contact when the button is pressed. Available in private chats only."""
    request_location: Optional[bool] = Field(default=None)
    """Optional. If True, the user's current location will be sent when the button is pressed. Available in private chats only."""
    request_poll: Optional[KeyboardButtonPollType] = Field(default=None)
    """Optional. If specified, the user will be asked to create a poll and send it to the bot when the button is pressed. Available in private chats only."""
    web_app: Optional[WebAppInfo] = Field(default=None)
    """Optional. If specified, the described Web App will be launched when the button is pressed. The Web App will be able to send a "web_app_data" service message. Available in private chats only."""

class KeyboardButtonRequestUsers(_Base, frozen=True):
    """This object defines the criteria used to request suitable users. Information about the selected users will be shared with the bot when the corresponding button is pressed. More about requesting users: https://core.telegram.org/bots/features#chat-and-user-selection
    
    https://core.telegram.org/bots/api#keyboardbuttonrequestusers
    """
    request_id: int
    """Signed 32-bit identifier of the request that will be received back in the UsersShared object. Must be unique within the message."""
    user_is_bot: Optional[bool] = Field(default=None)
    """Optional. Pass True to request bots, pass False to request regular users. If not specified, no additional restrictions are applied."""
    user_is_premium: Optional[bool] = Field(default=None)
    """Optional. Pass True to request premium users, pass False to request non-premium users. If not specified, no additional restrictions are applied."""
    max_quantity: Optional[int] = Field(default=None)
    """Optional. The maximum number of users to be selected; 1-10. Defaults to 1."""
    request_name: Optional[bool] = Field(default=None)
    """Optional. Pass True to request the users' first and last names"""
    request_username: Optional[bool] = Field(default=None)
    """Optional. Pass True to request the users' usernames"""
    request_photo: Optional[bool] = Field(default=None)
    """Optional. Pass True to request the users' photos"""

class KeyboardButtonRequestChat(_Base, frozen=True):
    """This object defines the criteria used to request a suitable chat. Information about the selected chat will be shared with the bot when the corresponding button is pressed. The bot will be granted requested rights in the chat if appropriate. More about requesting chats: https://core.telegram.org/bots/features#chat-and-user-selection.
    
    https://core.telegram.org/bots/api#keyboardbuttonrequestchat
    """
    request_id: int
    """Signed 32-bit identifier of the request, which will be received back in the ChatShared object. Must be unique within the message."""
    chat_is_channel: bool
    """Pass True to request a channel chat, pass False to request a group or a supergroup chat"""
    chat_is_forum: Optional[bool] = Field(default=None)
    """Optional. Pass True to request a forum supergroup, pass False to request a non-forum chat. If not specified, no additional restrictions are applied."""
    chat_has_username: Optional[bool] = Field(default=None)
    """Optional. Pass True to request a supergroup or a channel with a username, pass False to request a chat without a username. If not specified, no additional restrictions are applied."""
    chat_is_created: Optional[bool] = Field(default=None)
    """Optional. Pass True to request a chat owned by the user. Otherwise, no additional restrictions are applied."""
    user_administrator_rights: Optional[ChatAdministratorRights] = Field(default=None)
    """Optional. A JSON-serialized object listing the required administrator rights of the user in the chat. The rights must be a superset of bot_administrator_rights. If not specified, no additional restrictions are applied."""
    bot_administrator_rights: Optional[ChatAdministratorRights] = Field(default=None)
    """Optional. A JSON-serialized object listing the required administrator rights of the bot in the chat. The rights must be a subset of user_administrator_rights. If not specified, no additional restrictions are applied."""
    bot_is_member: Optional[bool] = Field(default=None)
    """Optional. Pass True to request a chat with the bot as a member. Otherwise, no additional restrictions are applied."""
    request_title: Optional[bool] = Field(default=None)
    """Optional. Pass True to request the chat's title"""
    request_username: Optional[bool] = Field(default=None)
    """Optional. Pass True to request the chat's username"""
    request_photo: Optional[bool] = Field(default=None)
    """Optional. Pass True to request the chat's photo"""

class KeyboardButtonRequestManagedBot(_Base, frozen=True):
    """This object defines the parameters for the creation of a managed bot. Information about the created bot will be shared with the bot using the update managed_bot and a Message with the field managed_bot_created.
    
    https://core.telegram.org/bots/api#keyboardbuttonrequestmanagedbot
    """
    request_id: int
    """Signed 32-bit identifier of the request. Must be unique within the message."""
    suggested_name: Optional[str] = Field(default=None)
    """Optional. Suggested name for the bot"""
    suggested_username: Optional[str] = Field(default=None)
    """Optional. Suggested username for the bot"""

class KeyboardButtonPollType(_Base, frozen=True):
    """This object represents type of a poll, which is allowed to be created and sent when the corresponding button is pressed.
    
    https://core.telegram.org/bots/api#keyboardbuttonpolltype
    """
    type: Optional[str] = Field(default=None)
    """Optional. If quiz is passed, the user will be allowed to create only polls in the quiz mode. If regular is passed, only regular polls will be allowed. Otherwise, the user will be allowed to create a poll of any type."""

class ReplyKeyboardRemove(_Base, frozen=True):
    """Upon receiving a message with this object, Telegram clients will remove the current custom keyboard and display the default letter-keyboard. By default, custom keyboards are displayed until a new keyboard is sent by a bot. An exception is made for one-time keyboards that are hidden immediately after the user presses a button (see ReplyKeyboardMarkup). Not supported in channels and for messages sent on behalf of a business account.
    
    https://core.telegram.org/bots/api#replykeyboardremove
    """
    remove_keyboard: bool
    """Requests clients to remove the custom keyboard (user will not be able to summon this keyboard; if you want to hide the keyboard from sight but keep it accessible, use one_time_keyboard in ReplyKeyboardMarkup)"""
    selective: Optional[bool] = Field(default=None)
    """Optional. Use this parameter if you want to remove the keyboard for specific users only. Targets: 1) users that are @mentioned in the text of the Message object; 2) if the bot's message is a reply to a message in the same chat and forum topic, sender of the original message. Example: A user votes in a poll, bot returns confirmation message in reply to the vote and removes the keyboard for that user, while still showing the keyboard with poll options to users who haven't voted yet."""

class InlineKeyboardMarkup(_Base, frozen=True):
    """This object represents an inline keyboard that appears right next to the message it belongs to.
    
    https://core.telegram.org/bots/api#inlinekeyboardmarkup
    """
    inline_keyboard: List[List[InlineKeyboardButton]]
    """Array of button rows, each represented by an Array of InlineKeyboardButton objects"""
    force_reply: Optional[bool] = Field(default=None)
    """Optional. Pass True if the reply interface must be shown to the user, as if they had manually selected the bot's message and tapped 'Reply'. The value of the field can't be changed when the inline keyboard is edited."""

class InlineKeyboardButton(_Base, frozen=True):
    """This object represents one button of an inline keyboard. Exactly one of the fields other than text, icon_custom_emoji_id, and style must be used to specify the type of the button.
    
    https://core.telegram.org/bots/api#inlinekeyboardbutton
    """
    text: str
    """Label text on the button"""
    icon_custom_emoji_id: Optional[str] = Field(default=None)
    """Optional. Unique identifier of the custom emoji shown before the text of the button. Can only be used by bots that purchased additional usernames on Fragment or in the messages directly sent by the bot to private, group and supergroup chats if the owner of the bot has a Telegram Premium subscription."""
    style: Optional[str] = Field(default=None)
    """Optional. Style of the button. Must be one of "danger" (red), "success" (green) or "primary" (blue). If omitted, then an app-specific style is used."""
    url: Optional[str] = Field(default=None)
    """Optional. HTTP or tg:// URL to be opened when the button is pressed. Links tg://user?id=<user_id> can be used to mention a user by their identifier without using a username, if this is allowed by their privacy settings."""
    callback_data: Optional[str] = Field(default=None)
    """Optional. Data to be sent in a callback query to the bot when the button is pressed, 1-64 bytes"""
    web_app: Optional[WebAppInfo] = Field(default=None)
    """Optional. Description of the Web App that will be launched when the user presses the button. The Web App will be able to send an arbitrary message on behalf of the user using the method answerWebAppQuery. Available only in private chats between a user and the bot. Not supported for messages sent on behalf of a business account."""
    login_url: Optional[LoginUrl] = Field(default=None)
    """Optional. An HTTPS URL used to automatically authorize the user. Can be used as a replacement for the Telegram Login Widget. Not supported for ephemeral messages."""
    switch_inline_query: Optional[str] = Field(default=None)
    """Optional. If set, pressing the button will prompt the user to select one of their chats, open that chat and insert the bot's username and the specified inline query in the input field. May be empty, in which case just the bot's username will be inserted. Not supported for messages sent in channel direct messages chats and on behalf of a business account."""
    switch_inline_query_current_chat: Optional[str] = Field(default=None)
    """Optional. If set, pressing the button will insert the bot's username and the specified inline query in the current chat's input field. May be empty, in which case only the bot's username will be inserted. This offers a quick way for the user to open your bot in inline mode in the same chat - good for selecting something from multiple options. Not supported in channels and for messages sent in channel direct messages chats and on behalf of a business account."""
    switch_inline_query_chosen_chat: Optional[SwitchInlineQueryChosenChat] = Field(default=None)
    """Optional. If set, pressing the button will prompt the user to select one of their chats of the specified type, open that chat and insert the bot's username and the specified inline query in the input field. Not supported for messages sent in channel direct messages chats and on behalf of a business account."""
    copy_text: Optional[CopyTextButton] = Field(default=None)
    """Optional. Description of the button that copies the specified text to the clipboard"""
    callback_game: Optional[CallbackGame] = Field(default=None)
    """Optional. Description of the game that will be launched when the user presses the button. NOTE: This type of button must always be the first button in the first row."""
    pay: Optional[bool] = Field(default=None)
    """Optional. Specify True, to send a Pay button. Substrings "⭐" and "XTR" in the buttons's text will be replaced with a Telegram Star icon. NOTE: This type of button must always be the first button in the first row and can only be used in invoice messages."""
    disabled: Optional[DisabledButton] = Field(default=None)
    """Optional. If set, then the button is disabled and does nothing"""

class LoginUrl(_Base, frozen=True):
    """This object represents a parameter of the inline keyboard button used to automatically authorize a user. It serves as a great replacement for the Telegram Login Widget when the user is coming from Telegram. All the user needs to do is tap/click a button and confirm that they want to log in:
    
    https://core.telegram.org/bots/api#loginurl
    """
    url: str
    """An HTTPS URL to be opened with user authorization data added to the query string when the button is pressed. If the user refuses to provide authorization data, the original URL without information about the user will be opened. The data added is the same as described in Receiving authorization data. NOTE: You must always check the hash of the received data to verify the authentication and the integrity of the data as described in Checking authorization."""
    forward_text: Optional[str] = Field(default=None)
    """Optional. New text of the button in forwarded messages"""
    bot_username: Optional[str] = Field(default=None)
    """Optional. Username of a bot, which will be used for user authorization; not supported in RichMessageButton. See Setting up a bot for more details. If not specified, the current bot's username will be assumed. The url's domain must be the same as the domain linked with the bot. See Linking your domain to the bot for more details."""
    request_write_access: Optional[bool] = Field(default=None)
    """Optional. Pass True to request the permission for your bot to send messages to the user"""

class SwitchInlineQueryChosenChat(_Base, frozen=True):
    """This object represents an inline button that switches the current user to inline mode in a chosen chat, with an optional default inline query.
    
    https://core.telegram.org/bots/api#switchinlinequerychosenchat
    """
    query: Optional[str] = Field(default=None)
    """Optional. The default inline query to be inserted in the input field. If left empty, only the bot's username will be inserted."""
    allow_user_chats: Optional[bool] = Field(default=None)
    """Optional. True, if private chats with users can be chosen"""
    allow_bot_chats: Optional[bool] = Field(default=None)
    """Optional. True, if private chats with bots can be chosen"""
    allow_group_chats: Optional[bool] = Field(default=None)
    """Optional. True, if group and supergroup chats can be chosen"""
    allow_channel_chats: Optional[bool] = Field(default=None)
    """Optional. True, if channel chats can be chosen"""

class CopyTextButton(_Base, frozen=True):
    """This object represents an inline keyboard button that copies specified text to the clipboard.
    
    https://core.telegram.org/bots/api#copytextbutton
    """
    text: str
    """The text to be copied to the clipboard; 1-256 characters"""

class DisabledButton(_Base, frozen=True):
    """This object represents a disabled button which does nothing. Currently holds no information.
    
    https://core.telegram.org/bots/api#disabledbutton
    """

class CallbackQuery(_Base, frozen=True):
    """This object represents an incoming callback query from a callback button in an inline keyboard. If the button that originated the query was attached to a message sent by the bot, the field message will be present. If the button was attached to a message sent via the bot (in inline mode), the field inline_message_id will be present. Exactly one of the fields data or game_short_name will be present.
    
    https://core.telegram.org/bots/api#callbackquery
    """
    id: str
    """Unique identifier for this query"""
    user: User = Field(alias='from')
    """Sender"""
    message: Optional[MaybeInaccessibleMessage] = Field(default=None)
    """Optional. Message sent by the bot with the callback button that originated the query"""
    inline_message_id: Optional[str] = Field(default=None)
    """Optional. Identifier of the message sent via the bot in inline mode, that originated the query"""
    chat_instance: str
    """Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent. Useful for high scores in games."""
    data: Optional[str] = Field(default=None)
    """Optional. Data associated with the callback button. Be aware that the message originated the query can contain no callback buttons with this data."""
    game_short_name: Optional[str] = Field(default=None)
    """Optional. Short name of a Game to be returned, serves as the unique identifier for the game"""

    async def answer(
        self,
        text: Optional[str] = None,
        *,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None,
    ) -> bool:
        """Как bot.answer_callback_query(), но id запроса берётся из объекта.
        
        Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. On success, True is returned.
        
        https://core.telegram.org/bots/api#answercallbackquery
        """
        return await self._require_bot().answer_callback_query(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )

class ForceReply(_Base, frozen=True):
    """Upon receiving a message with this object, Telegram clients will display a reply interface to the user (act as if the user has selected the bot's message and tapped 'Reply'). This can be extremely useful if you want to create user-friendly step-by-step interfaces without having to sacrifice privacy mode. Not supported in channels and for messages sent on behalf of a user account.
    
    https://core.telegram.org/bots/api#forcereply
    """
    force_reply: bool
    """Shows reply interface to the user, as if they had manually selected the bot's message and tapped 'Reply'"""
    input_field_placeholder: Optional[str] = Field(default=None)
    """Optional. The placeholder to be shown in the input field when the reply is active; 1-64 characters"""
    selective: Optional[bool] = Field(default=None)
    """Optional. Use this parameter if you want to force reply from specific users only. Targets: 1) users that are @mentioned in the text of the Message object; 2) if the bot's message is a reply to a message in the same chat and forum topic, sender of the original message."""

class Community(_Base, frozen=True):
    """Represents a community (a group of chats).
    
    https://core.telegram.org/bots/api#community
    """
    id: int
    """Unique identifier for this community. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier."""
    name: str
    """Name of the community"""

class ChatPhoto(_Base, frozen=True):
    """This object represents a chat photo.
    
    https://core.telegram.org/bots/api#chatphoto
    """
    small_file_id: str
    """File identifier of small (160x160) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed."""
    small_file_unique_id: str
    """Unique file identifier of small (160x160) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    big_file_id: str
    """File identifier of big (640x640) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed."""
    big_file_unique_id: str
    """Unique file identifier of big (640x640) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""

class ChatInviteLink(_Base, frozen=True):
    """Represents an invite link for a chat.
    
    https://core.telegram.org/bots/api#chatinvitelink
    """
    invite_link: str
    """The invite link. If the link was created by another chat administrator, then the second part of the link will be replaced with "..."."""
    creator: User
    """Creator of the link"""
    creates_join_request: bool
    """True, if users joining the chat via the link need to be approved by chat administrators"""
    is_primary: bool
    """True, if the link is primary"""
    is_revoked: bool
    """True, if the link is revoked"""
    name: Optional[str] = Field(default=None)
    """Optional. Invite link name"""
    expire_date: Optional[int] = Field(default=None)
    """Optional. Point in time (Unix timestamp) when the link will expire or has been expired"""
    member_limit: Optional[int] = Field(default=None)
    """Optional. The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999"""
    pending_join_request_count: Optional[int] = Field(default=None)
    """Optional. Number of pending join requests created using this link"""
    subscription_period: Optional[int] = Field(default=None)
    """Optional. The number of seconds the subscription will be active for before the next payment"""
    subscription_price: Optional[int] = Field(default=None)
    """Optional. The amount of Telegram Stars a user must pay initially and after each subsequent subscription period to be a member of the chat using the link"""

class ChatAdministratorRights(_Base, frozen=True):
    """Represents the rights of an administrator in a chat.
    
    https://core.telegram.org/bots/api#chatadministratorrights
    """
    is_anonymous: bool
    """True, if the user's presence in the chat is hidden"""
    can_manage_chat: bool
    """True, if the administrator can access the chat event log, get boost list, see hidden supergroup and channel members, report spam messages, ignore slow mode, and send messages to the chat without paying Telegram Stars. Implied by any other administrator privilege."""
    can_delete_messages: bool
    """True, if the administrator can delete messages of other users"""
    can_manage_video_chats: bool
    """True, if the administrator can manage video chats"""
    can_restrict_members: bool
    """True, if the administrator can restrict, ban or unban chat members, or access supergroup statistics"""
    can_promote_members: bool
    """True, if the administrator can add new administrators with a subset of their own privileges or demote administrators that they have promoted, directly or indirectly (promoted by administrators that were appointed by the user)"""
    can_change_info: bool
    """True, if the user is allowed to change the chat title, photo and other settings"""
    can_invite_users: bool
    """True, if the user is allowed to invite new users to the chat"""
    can_post_stories: bool
    """True, if the administrator can post stories to the chat"""
    can_edit_stories: bool
    """True, if the administrator can edit stories posted by other users, post stories to the chat page, pin chat stories, and access the chat's story archive"""
    can_delete_stories: bool
    """True, if the administrator can delete stories posted by other users"""
    can_post_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the administrator can post messages in the channel, approve suggested posts, or access channel statistics; for channels only"""
    can_edit_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the administrator can edit messages of other users and can pin messages; for channels only"""
    can_pin_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to pin messages; for groups and supergroups only"""
    can_manage_topics: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to create, rename, close, and reopen forum topics; for supergroups only"""
    can_manage_direct_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the administrator can manage direct messages of the channel and decline suggested posts; for channels only"""
    can_manage_tags: Optional[bool] = Field(default=None)
    """Optional. True, if the administrator can edit the tags of regular members; for groups and supergroups only"""
    can_send_welcome_messages: bool
    """True, if the administrator can manage chat welcome messages or directly send them in the case of bots"""

class ChatMemberUpdated(_Base, frozen=True):
    """This object represents changes in the status of a chat member.
    
    https://core.telegram.org/bots/api#chatmemberupdated
    """
    chat: Chat
    """Chat the user belongs to"""
    user: User = Field(alias='from')
    """Performer of the action, which resulted in the change"""
    date: int
    """Date the change was done in Unix time"""
    old_chat_member: ChatMember
    """Previous information about the chat member"""
    new_chat_member: ChatMember
    """New information about the chat member"""
    invite_link: Optional[ChatInviteLink] = Field(default=None)
    """Optional. Chat invite link, which was used by the user to join the chat; for joining by invite link events only"""
    via_join_request: Optional[bool] = Field(default=None)
    """Optional. True, if the user joined the chat after sending a direct join request without using an invite link and being approved by an administrator"""
    via_chat_folder_invite_link: Optional[bool] = Field(default=None)
    """Optional. True, if the user joined the chat via a chat folder invite link"""

    async def answer(
        self,
        text: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_message(), но чат — чат этого события.
        
        Use this method to send text messages. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendmessage
        """
        return await self._require_bot().send_message(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_photo(
        self,
        photo: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_photo(), но чат — чат этого события.
        
        Use this method to send photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendphoto
        """
        return await self._require_bot().send_photo(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_live_photo(
        self,
        live_photo: Union[InputFile, str],
        photo: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_live_photo(), но чат — чат этого события.
        
        Use this method to send live photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlivephoto
        """
        return await self._require_bot().send_live_photo(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            live_photo=live_photo,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_audio(
        self,
        audio: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_audio(), но чат — чат этого события.
        
        Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .MP3 or .M4A format. On success, the sent Message is returned. Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.
        
        For sending voice messages, use the sendVoice method instead.
        
        https://core.telegram.org/bots/api#sendaudio
        """
        return await self._require_bot().send_audio(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_document(
        self,
        document: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_document(), но чат — чат этого события.
        
        Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#senddocument
        """
        return await self._require_bot().send_document(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            document=document,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_video(
        self,
        video: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        cover: Optional[Union[InputFile, str]] = None,
        start_timestamp: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_video(), но чат — чат этого события.
        
        Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvideo
        """
        return await self._require_bot().send_video(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            video=video,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            cover=cover,
            start_timestamp=start_timestamp,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_animation(
        self,
        animation: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_animation(), но чат — чат этого события.
        
        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendanimation
        """
        return await self._require_bot().send_animation(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            animation=animation,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_voice(
        self,
        voice: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_voice(), но чат — чат этого события.
        
        Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other formats may be sent as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvoice
        """
        return await self._require_bot().send_voice(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_video_note(
        self,
        video_note: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_video_note(), но чат — чат этого события.
        
        Use this method to send a rounded square MPEG4 video of up to 1 minute long. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvideonote
        """
        return await self._require_bot().send_video_note(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            video_note=video_note,
            duration=duration,
            length=length,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_paid_media(
        self,
        star_count: int,
        media: List[InputPaidMedia],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        payload: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_paid_media(), но чат — чат этого события.
        
        Use this method to send paid media. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpaidmedia
        """
        return await self._require_bot().send_paid_media(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            star_count=star_count,
            media=media,
            payload=payload,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_media_group(
        self,
        media: Union[List[InputMediaAudio], List[InputMediaDocument], List[InputMediaLivePhoto], List[InputMediaPhoto], List[InputMediaVideo]],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
    ) -> List[Message]:
        """Как bot.send_media_group(), но чат — чат этого события.
        
        Use this method to send a group of photos, live photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an Array of Message objects that were sent is returned.
        
        https://core.telegram.org/bots/api#sendmediagroup
        """
        return await self._require_bot().send_media_group(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
        )

    async def answer_location(
        self,
        latitude: float,
        longitude: float,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_location(), но чат — чат этого события.
        
        Use this method to send point on the map. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlocation
        """
        return await self._require_bot().send_location(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_venue(), но чат — чат этого события.
        
        Use this method to send information about a venue. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvenue
        """
        return await self._require_bot().send_venue(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_contact(
        self,
        phone_number: str,
        first_name: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_contact(), но чат — чат этого события.
        
        Use this method to send phone contacts. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendcontact
        """
        return await self._require_bot().send_contact(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_poll(
        self,
        question: str,
        options: List[InputPollOption],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        question_parse_mode: Optional[str] = None,
        question_entities: Optional[List[MessageEntity]] = None,
        is_anonymous: Optional[bool] = None,
        type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        allows_revoting: Optional[bool] = None,
        shuffle_options: Optional[bool] = None,
        allow_adding_options: Optional[bool] = None,
        hide_results_until_closes: Optional[bool] = None,
        members_only: Optional[bool] = None,
        country_codes: Optional[List[str]] = None,
        correct_option_ids: Optional[List[int]] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[str] = None,
        explanation_entities: Optional[List[MessageEntity]] = None,
        explanation_media: Optional[InputPollMedia] = None,
        open_period: Optional[int] = None,
        close_date: Optional[int] = None,
        is_closed: Optional[bool] = None,
        description: Optional[str] = None,
        description_parse_mode: Optional[str] = None,
        description_entities: Optional[List[MessageEntity]] = None,
        media: Optional[InputPollMedia] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_poll(), но чат — чат этого события.
        
        Use this method to send a native poll. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpoll
        """
        return await self._require_bot().send_poll(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            question=question,
            question_parse_mode=question_parse_mode,
            question_entities=question_entities,
            options=options,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            allows_revoting=allows_revoting,
            shuffle_options=shuffle_options,
            allow_adding_options=allow_adding_options,
            hide_results_until_closes=hide_results_until_closes,
            members_only=members_only,
            country_codes=country_codes,
            correct_option_ids=correct_option_ids,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            explanation_media=explanation_media,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            description=description,
            description_parse_mode=description_parse_mode,
            description_entities=description_entities,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_checklist(
        self,
        business_connection_id: str,
        checklist: InputChecklist,
        *,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_checklist(), но чат — чат этого события.
        
        Use this method to send a checklist on behalf of a connected business account. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendchecklist
        """
        return await self._require_bot().send_checklist(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            checklist=checklist,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_dice(
        self,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_dice(), но чат — чат этого события.
        
        Use this method to send an animated emoji that will display a random value. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#senddice
        """
        return await self._require_bot().send_dice(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_message_draft(
        self,
        draft_id: int,
        *,
        message_thread_id: Optional[int] = None,
        text: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        can_stop: Optional[bool] = None,
        keep_on_stop: Optional[bool] = None,
    ) -> bool:
        """Как bot.send_message_draft(), но чат — чат этого события.
        
        Use this method to stream a partial message to a user while the message is being generated. Note that the streamed draft is ephemeral and acts as a temporary 30-second preview - once the output is finalized, you must call sendMessage with the complete message to persist it in the user's chat. Returns True on success.
        
        https://core.telegram.org/bots/api#sendmessagedraft
        """
        return await self._require_bot().send_message_draft(
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            draft_id=draft_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            can_stop=can_stop,
            keep_on_stop=keep_on_stop,
        )

    async def answer_chat_action(
        self,
        action: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> bool:
        """Как bot.send_chat_action(), но чат — чат этого события.
        
        Use this method when you need to tell the user that something is happening on the bot's side. The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status). Returns True on success.
        
        We only recommend using this method when a response from the bot will take a noticeable amount of time to arrive.
        
        https://core.telegram.org/bots/api#sendchataction
        """
        return await self._require_bot().send_chat_action(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            action=action,
        )

    async def answer_sticker(
        self,
        sticker: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_sticker(), но чат — чат этого события.
        
        Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendsticker
        """
        return await self._require_bot().send_sticker(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            sticker=sticker,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_rich_message(
        self,
        rich_message: InputRichMessage,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_rich_message(), но чат — чат этого события.
        
        Use this method to send rich messages. If the message contains a block with a media element, then the bot must have the right to send the media to the chat. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendrichmessage
        """
        return await self._require_bot().send_rich_message(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            rich_message=rich_message,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_rich_message_draft(
        self,
        draft_id: int,
        rich_message: InputRichMessage,
        *,
        message_thread_id: Optional[int] = None,
        can_stop: Optional[bool] = None,
        keep_on_stop: Optional[bool] = None,
    ) -> bool:
        """Как bot.send_rich_message_draft(), но чат — чат этого события.
        
        Use this method to stream a partial rich message to a user while the message is being generated. Note that the streamed draft is ephemeral and acts as a temporary 30-second preview - once the output is finalized, you must call sendRichMessage with the complete message to persist it in the user's chat. Returns True on success.
        
        https://core.telegram.org/bots/api#sendrichmessagedraft
        """
        return await self._require_bot().send_rich_message_draft(
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            draft_id=draft_id,
            rich_message=rich_message,
            can_stop=can_stop,
            keep_on_stop=keep_on_stop,
        )

    async def answer_invoice(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: List[LabeledPrice],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        provider_token: Optional[str] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
        start_parameter: Optional[str] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_invoice(), но чат — чат этого события.
        
        Use this method to send invoices. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendinvoice
        """
        return await self._require_bot().send_invoice(
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            start_parameter=start_parameter,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def answer_game(
        self,
        game_short_name: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_game(), но чат — чат этого события.
        
        Use this method to send a game. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendgame
        """
        return await self._require_bot().send_game(
            business_connection_id=business_connection_id,
            chat_id=self.chat.id,
            message_thread_id=message_thread_id,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

class ChatMemberOwner(_Base, frozen=True):
    """Represents a chat member that owns the chat and has all administrator privileges.
    
    https://core.telegram.org/bots/api#chatmemberowner
    """
    status: Literal["creator"] = Field(default='creator')
    """The member's status in the chat, always "creator" """
    user: User
    """Information about the user"""
    is_anonymous: bool
    """True, if the user's presence in the chat is hidden"""
    custom_title: Optional[str] = Field(default=None)
    """Optional. Custom title for this user"""

class ChatMemberAdministrator(_Base, frozen=True):
    """Represents a chat member that has some additional privileges.
    
    https://core.telegram.org/bots/api#chatmemberadministrator
    """
    status: Literal["administrator"] = Field(default='administrator')
    """The member's status in the chat, always "administrator" """
    user: User
    """Information about the user"""
    can_be_edited: bool
    """True, if the bot is allowed to edit administrator privileges of that user"""
    is_anonymous: bool
    """True, if the user's presence in the chat is hidden"""
    can_manage_chat: bool
    """True, if the administrator can access the chat event log, get boost list, see hidden supergroup and channel members, report spam messages, ignore slow mode, and send messages to the chat without paying Telegram Stars. Implied by any other administrator privilege."""
    can_delete_messages: bool
    """True, if the administrator can delete messages of other users"""
    can_manage_video_chats: bool
    """True, if the administrator can manage video chats"""
    can_restrict_members: bool
    """True, if the administrator can restrict, ban or unban chat members, or access supergroup statistics"""
    can_promote_members: bool
    """True, if the administrator can add new administrators with a subset of their own privileges or demote administrators that they have promoted, directly or indirectly (promoted by administrators that were appointed by the user)"""
    can_change_info: bool
    """True, if the user is allowed to change the chat title, photo and other settings"""
    can_invite_users: bool
    """True, if the user is allowed to invite new users to the chat"""
    can_post_stories: bool
    """True, if the administrator can post stories to the chat"""
    can_edit_stories: bool
    """True, if the administrator can edit stories posted by other users, post stories to the chat page, pin chat stories, and access the chat's story archive"""
    can_delete_stories: bool
    """True, if the administrator can delete stories posted by other users"""
    can_post_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the administrator can post messages in the channel, approve suggested posts, or access channel statistics; for channels only"""
    can_edit_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the administrator can edit messages of other users and can pin messages; for channels only"""
    can_pin_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to pin messages; for groups and supergroups only"""
    can_manage_topics: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to create, rename, close, and reopen forum topics; for supergroups only"""
    can_manage_direct_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the administrator can manage direct messages of the channel and decline suggested posts; for channels only"""
    can_manage_tags: Optional[bool] = Field(default=None)
    """Optional. True, if the administrator can edit the tags of regular members; for groups and supergroups only"""
    can_send_welcome_messages: bool
    """True, if the administrator can manage chat welcome messages or directly send them in the case of bots"""
    custom_title: Optional[str] = Field(default=None)
    """Optional. Custom title for this user"""

class ChatMemberMember(_Base, frozen=True):
    """Represents a chat member that has no additional privileges or restrictions.
    
    https://core.telegram.org/bots/api#chatmembermember
    """
    status: Literal["member"] = Field(default='member')
    """The member's status in the chat, always "member" """
    tag: Optional[str] = Field(default=None)
    """Optional. Tag of the member"""
    user: User
    """Information about the user"""
    until_date: Optional[int] = Field(default=None)
    """Optional. Date when the user's subscription will expire; Unix time"""

class ChatMemberRestricted(_Base, frozen=True):
    """Represents a chat member that is under certain restrictions in the chat. Supergroups only.
    
    https://core.telegram.org/bots/api#chatmemberrestricted
    """
    status: Literal["restricted"] = Field(default='restricted')
    """The member's status in the chat, always "restricted" """
    tag: Optional[str] = Field(default=None)
    """Optional. Tag of the member"""
    user: User
    """Information about the user"""
    is_member: bool
    """True, if the user is a member of the chat at the moment of the request"""
    can_send_messages: bool
    """True, if the user is allowed to send text messages, rich messages, contacts, giveaways, giveaway winners, invoices, locations and venues"""
    can_send_audios: bool
    """True, if the user is allowed to send audios"""
    can_send_documents: bool
    """True, if the user is allowed to send documents"""
    can_send_photos: bool
    """True, if the user is allowed to send photos"""
    can_send_videos: bool
    """True, if the user is allowed to send videos"""
    can_send_video_notes: bool
    """True, if the user is allowed to send video notes"""
    can_send_voice_notes: bool
    """True, if the user is allowed to send voice notes"""
    can_send_polls: bool
    """True, if the user is allowed to send polls and checklists"""
    can_send_other_messages: bool
    """True, if the user is allowed to send animations, games, stickers and use inline bots"""
    can_add_web_page_previews: bool
    """True, if the user is allowed to add web page previews to their messages"""
    can_react_to_messages: bool
    """True, if the user is allowed to react to messages"""
    can_edit_tag: bool
    """True, if the user is allowed to edit their own tag"""
    can_change_info: bool
    """True, if the user is allowed to change the chat title, photo and other settings"""
    can_invite_users: bool
    """True, if the user is allowed to invite new users to the chat"""
    can_pin_messages: bool
    """True, if the user is allowed to pin messages"""
    can_manage_topics: bool
    """True, if the user is allowed to create forum topics"""
    until_date: int
    """Date when restrictions will be lifted for this user; Unix time. If 0, then the user is restricted forever."""

class ChatMemberLeft(_Base, frozen=True):
    """Represents a chat member that isn't currently a member of the chat, but may join it themselves.
    
    https://core.telegram.org/bots/api#chatmemberleft
    """
    status: Literal["left"] = Field(default='left')
    """The member's status in the chat, always "left" """
    user: User
    """Information about the user"""

class ChatMemberBanned(_Base, frozen=True):
    """Represents a chat member that was banned in the chat and can't return to the chat or view chat messages.
    
    https://core.telegram.org/bots/api#chatmemberbanned
    """
    status: Literal["kicked"] = Field(default='kicked')
    """The member's status in the chat, always "kicked" """
    user: User
    """Information about the user"""
    until_date: int
    """Date when restrictions will be lifted for this user; Unix time. If 0, then the user is banned forever."""

class ChatJoinRequest(_Base, frozen=True):
    """Represents a join request sent to a chat.
    
    https://core.telegram.org/bots/api#chatjoinrequest
    """
    chat: Chat
    """Chat to which the request was sent"""
    user: User = Field(alias='from')
    """User that sent the join request"""
    user_chat_id: int
    """Identifier of a private chat with the user who sent the join request. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier. The bot can use this identifier for 5 minutes to send messages until the join request is processed, assuming no other administrator contacted the user."""
    date: int
    """Date the request was sent in Unix time"""
    bio: Optional[str] = Field(default=None)
    """Optional. Bio of the user"""
    invite_link: Optional[ChatInviteLink] = Field(default=None)
    """Optional. Chat invite link that was used by the user to send the join request"""
    query_id: Optional[str] = Field(default=None)
    """Optional. Identifier of the join request query; for bots assigned to process join requests only. If present, then the bot must call sendChatJoinRequestWebApp or directly call answerChatJoinRequestQuery within 10 seconds."""

class ChatPermissions(_Base, frozen=True):
    """Describes actions that a non-administrator user is allowed to take in a chat.
    
    https://core.telegram.org/bots/api#chatpermissions
    """
    can_send_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to send text messages, rich messages, contacts, giveaways, giveaway winners, invoices, locations and venues"""
    can_send_audios: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to send audios"""
    can_send_documents: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to send documents"""
    can_send_photos: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to send photos"""
    can_send_videos: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to send videos"""
    can_send_video_notes: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to send video notes"""
    can_send_voice_notes: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to send voice notes"""
    can_send_polls: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to send polls and checklists"""
    can_send_other_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to send animations, games, stickers and use inline bots"""
    can_add_web_page_previews: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to add web page previews to their messages"""
    can_react_to_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to react to messages. If omitted, defaults to the value of can_send_messages."""
    can_edit_tag: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to edit their own tag. If omitted, defaults to the value of can_pin_messages."""
    can_change_info: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to change the chat title, photo and other settings. Ignored in public supergroups."""
    can_invite_users: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to invite new users to the chat"""
    can_pin_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to pin messages. Ignored in public supergroups."""
    can_manage_topics: Optional[bool] = Field(default=None)
    """Optional. True, if the user is allowed to create forum topics. If omitted, defaults to the value of can_pin_messages."""

class Birthdate(_Base, frozen=True):
    """Describes the birthdate of a user.
    
    https://core.telegram.org/bots/api#birthdate
    """
    day: int
    """Day of the user's birth; 1-31"""
    month: int
    """Month of the user's birth; 1-12"""
    year: Optional[int] = Field(default=None)
    """Optional. Year of the user's birth"""

class BusinessIntro(_Base, frozen=True):
    """Contains information about the start page settings of a Telegram Business account.
    
    https://core.telegram.org/bots/api#businessintro
    """
    title: Optional[str] = Field(default=None)
    """Optional. Title text of the business intro"""
    message: Optional[str] = Field(default=None)
    """Optional. Message text of the business intro"""
    sticker: Optional[Sticker] = Field(default=None)
    """Optional. Sticker of the business intro"""

class BusinessLocation(_Base, frozen=True):
    """Contains information about the location of a Telegram Business account.
    
    https://core.telegram.org/bots/api#businesslocation
    """
    address: str
    """Address of the business"""
    location: Optional[Location] = Field(default=None)
    """Optional. Location of the business"""

class BusinessOpeningHoursInterval(_Base, frozen=True):
    """Describes an interval of time during which a business is open.
    
    https://core.telegram.org/bots/api#businessopeninghoursinterval
    """
    opening_minute: int
    """The minute's sequence number in a week, starting on Monday, marking the start of the time interval during which the business is open; 0 - 7 * 24 * 60"""
    closing_minute: int
    """The minute's sequence number in a week, starting on Monday, marking the end of the time interval during which the business is open; 0 - 8 * 24 * 60"""

class BusinessOpeningHours(_Base, frozen=True):
    """Describes the opening hours of a business.
    
    https://core.telegram.org/bots/api#businessopeninghours
    """
    time_zone_name: str
    """Unique name of the time zone for which the opening hours are defined"""
    opening_hours: List[BusinessOpeningHoursInterval]
    """List of time intervals describing business opening hours"""

class UserRating(_Base, frozen=True):
    """This object describes the rating of a user based on their Telegram Star spendings.
    
    https://core.telegram.org/bots/api#userrating
    """
    level: int
    """Current level of the user, indicating their reliability when purchasing digital goods and services. A higher level suggests a more trustworthy customer; a negative level is likely reason for concern."""
    rating: int
    """Numerical value of the user's rating; the higher the rating, the better"""
    current_level_rating: int
    """The rating value required to get the current level"""
    next_level_rating: Optional[int] = Field(default=None)
    """Optional. The rating value required to get to the next level; omitted if the maximum level was reached"""

class StoryAreaPosition(_Base, frozen=True):
    """Describes the position of a clickable area within a story.
    
    https://core.telegram.org/bots/api#storyareaposition
    """
    x_percentage: float
    """The abscissa of the area's center, as a percentage of the media width"""
    y_percentage: float
    """The ordinate of the area's center, as a percentage of the media height"""
    width_percentage: float
    """The width of the area's rectangle, as a percentage of the media width"""
    height_percentage: float
    """The height of the area's rectangle, as a percentage of the media height"""
    rotation_angle: float
    """The clockwise rotation angle of the rectangle, in degrees; 0-360"""
    corner_radius_percentage: float
    """The radius of the rectangle corner rounding, as a percentage of the media width"""

class LocationAddress(_Base, frozen=True):
    """Describes the physical address of a location.
    
    https://core.telegram.org/bots/api#locationaddress
    """
    country_code: str
    """The two-letter ISO 3166-1 alpha-2 country code of the country where the location is located"""
    state: Optional[str] = Field(default=None)
    """Optional. State of the location"""
    city: Optional[str] = Field(default=None)
    """Optional. City of the location"""
    street: Optional[str] = Field(default=None)
    """Optional. Street address of the location"""

class StoryAreaTypeLocation(_Base, frozen=True):
    """Describes a story area pointing to a location. Currently, a story can have up to 10 location areas.
    
    https://core.telegram.org/bots/api#storyareatypelocation
    """
    type: Literal["location"] = Field(default='location')
    """Type of the area, always "location" """
    latitude: float
    """Location latitude in degrees"""
    longitude: float
    """Location longitude in degrees"""
    address: Optional[LocationAddress] = Field(default=None)
    """Optional. Address of the location"""

class StoryAreaTypeSuggestedReaction(_Base, frozen=True):
    """Describes a story area pointing to a suggested reaction. Currently, a story can have up to 5 suggested reaction areas.
    
    https://core.telegram.org/bots/api#storyareatypesuggestedreaction
    """
    type: Literal["suggested_reaction"] = Field(default='suggested_reaction')
    """Type of the area, always "suggested_reaction" """
    reaction_type: ReactionType
    """Type of the reaction"""
    is_dark: Optional[bool] = Field(default=None)
    """Optional. Pass True if the reaction area has a dark background"""
    is_flipped: Optional[bool] = Field(default=None)
    """Optional. Pass True if reaction area corner is flipped"""

class StoryAreaTypeLink(_Base, frozen=True):
    """Describes a story area pointing to an HTTP or tg:// link. Currently, a story can have up to 3 link areas.
    
    https://core.telegram.org/bots/api#storyareatypelink
    """
    type: Literal["link"] = Field(default='link')
    """Type of the area, always "link" """
    url: str
    """HTTP or tg:// URL to be opened when the area is clicked"""

class StoryAreaTypeWeather(_Base, frozen=True):
    """Describes a story area containing weather information. Currently, a story can have up to 3 weather areas.
    
    https://core.telegram.org/bots/api#storyareatypeweather
    """
    type: Literal["weather"] = Field(default='weather')
    """Type of the area, always "weather" """
    temperature: float
    """Temperature, in degree Celsius"""
    emoji: str
    """Emoji representing the weather"""
    background_color: int
    """A color of the area background in the ARGB format"""

class StoryAreaTypeUniqueGift(_Base, frozen=True):
    """Describes a story area pointing to a unique gift. Currently, a story can have at most 1 unique gift area.
    
    https://core.telegram.org/bots/api#storyareatypeuniquegift
    """
    type: Literal["unique_gift"] = Field(default='unique_gift')
    """Type of the area, always "unique_gift" """
    name: str
    """Unique name of the gift"""

class StoryArea(_Base, frozen=True):
    """Describes a clickable area on a story media.
    
    https://core.telegram.org/bots/api#storyarea
    """
    position: StoryAreaPosition
    """Position of the area"""
    type: StoryAreaType
    """Type of the area"""

class ChatLocation(_Base, frozen=True):
    """Represents a location to which a chat is connected.
    
    https://core.telegram.org/bots/api#chatlocation
    """
    location: Location
    """The location to which the supergroup is connected. Can't be a live location."""
    address: str
    """Location address; 1-64 characters, as defined by the chat owner"""

class ReactionTypeEmoji(_Base, frozen=True):
    """The reaction is based on an emoji.
    
    https://core.telegram.org/bots/api#reactiontypeemoji
    """
    type: Literal["emoji"] = Field(default='emoji')
    """Type of the reaction, always "emoji" """
    emoji: str
    """Reaction emoji. Currently, it can be one of "❤", "👍", "👎", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", "❤‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝", "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂", "🤷", "🤷‍♀", "😡"."""

class ReactionTypeCustomEmoji(_Base, frozen=True):
    """The reaction is based on a custom emoji.
    
    https://core.telegram.org/bots/api#reactiontypecustomemoji
    """
    type: Literal["custom_emoji"] = Field(default='custom_emoji')
    """Type of the reaction, always "custom_emoji" """
    custom_emoji_id: str
    """Custom emoji identifier"""

class ReactionTypePaid(_Base, frozen=True):
    """The reaction is paid.
    
    https://core.telegram.org/bots/api#reactiontypepaid
    """
    type: Literal["paid"] = Field(default='paid')
    """Type of the reaction, always "paid" """

class ReactionCount(_Base, frozen=True):
    """Represents a reaction added to a message along with the number of times it was added.
    
    https://core.telegram.org/bots/api#reactioncount
    """
    type: ReactionType
    """Type of the reaction"""
    total_count: int
    """Number of times the reaction was added"""

class MessageReactionUpdated(_Base, frozen=True):
    """This object represents a change of a reaction on a message performed by a user.
    
    https://core.telegram.org/bots/api#messagereactionupdated
    """
    chat: Chat
    """The chat containing the message the user reacted to"""
    message_id: int
    """Unique identifier of the message inside the chat"""
    user: Optional[User] = Field(default=None)
    """Optional. The user that changed the reaction, if the user isn't anonymous"""
    actor_chat: Optional[Chat] = Field(default=None)
    """Optional. The chat on behalf of which the reaction was changed, if the user is anonymous"""
    date: int
    """Date of the change in Unix time"""
    old_reaction: List[ReactionType]
    """Previous list of reaction types that were set by the user"""
    new_reaction: List[ReactionType]
    """New list of reaction types that have been set by the user"""

class MessageReactionCountUpdated(_Base, frozen=True):
    """This object represents reaction changes on a message with anonymous reactions.
    
    https://core.telegram.org/bots/api#messagereactioncountupdated
    """
    chat: Chat
    """The chat containing the message"""
    message_id: int
    """Unique message identifier inside the chat"""
    date: int
    """Date of the change in Unix time"""
    reactions: List[ReactionCount]
    """List of reactions that are present on the message"""

class ForumTopic(_Base, frozen=True):
    """This object represents a forum topic.
    
    https://core.telegram.org/bots/api#forumtopic
    """
    message_thread_id: int
    """Unique identifier of the forum topic"""
    name: str
    """Name of the topic"""
    icon_color: int
    """Color of the topic icon in RGB format"""
    icon_custom_emoji_id: Optional[str] = Field(default=None)
    """Optional. Unique identifier of the custom emoji shown as the topic icon"""
    is_name_implicit: Optional[bool] = Field(default=None)
    """Optional. True, if the name of the topic wasn't specified explicitly by its creator and likely needs to be changed by the bot"""

class GiftBackground(_Base, frozen=True):
    """This object describes the background of a gift.
    
    https://core.telegram.org/bots/api#giftbackground
    """
    center_color: int
    """Center color of the background in RGB format"""
    edge_color: int
    """Edge color of the background in RGB format"""
    text_color: int
    """Text color of the background in RGB format"""

class Gift(_Base, frozen=True):
    """This object represents a gift that can be sent by the bot.
    
    https://core.telegram.org/bots/api#gift
    """
    id: str
    """Unique identifier of the gift"""
    sticker: Sticker
    """The sticker that represents the gift"""
    star_count: int
    """The number of Telegram Stars that must be paid to send the sticker"""
    upgrade_star_count: Optional[int] = Field(default=None)
    """Optional. The number of Telegram Stars that must be paid to upgrade the gift to a unique one"""
    is_premium: Optional[bool] = Field(default=None)
    """Optional. True, if the gift can only be purchased by Telegram Premium subscribers"""
    has_colors: Optional[bool] = Field(default=None)
    """Optional. True, if the gift can be used (after being upgraded) to customize a user's appearance"""
    total_count: Optional[int] = Field(default=None)
    """Optional. The total number of gifts of this type that can be sent by all users; for limited gifts only"""
    remaining_count: Optional[int] = Field(default=None)
    """Optional. The number of remaining gifts of this type that can be sent by all users; for limited gifts only"""
    personal_total_count: Optional[int] = Field(default=None)
    """Optional. The total number of gifts of this type that can be sent by the bot; for limited gifts only"""
    personal_remaining_count: Optional[int] = Field(default=None)
    """Optional. The number of remaining gifts of this type that can be sent by the bot; for limited gifts only"""
    background: Optional[GiftBackground] = Field(default=None)
    """Optional. Background of the gift"""
    unique_gift_variant_count: Optional[int] = Field(default=None)
    """Optional. The total number of different unique gifts that can be obtained by upgrading the gift"""
    publisher_chat: Optional[Chat] = Field(default=None)
    """Optional. Information about the chat that published the gift"""

class Gifts(_Base, frozen=True):
    """This object represent a list of gifts.
    
    https://core.telegram.org/bots/api#gifts
    """
    gifts: List[Gift]
    """The list of gifts"""

class UniqueGiftModel(_Base, frozen=True):
    """This object describes the model of a unique gift.
    
    https://core.telegram.org/bots/api#uniquegiftmodel
    """
    name: str
    """Name of the model"""
    sticker: Sticker
    """The sticker that represents the unique gift"""
    rarity_per_mille: int
    """The number of unique gifts that receive this model for every 1000 gift upgrades. Always 0 for crafted gifts."""
    rarity: Optional[str] = Field(default=None)
    """Optional. Rarity of the model if it is a crafted model. Currently, can be "uncommon", "rare", "epic", or "legendary"."""

class UniqueGiftSymbol(_Base, frozen=True):
    """This object describes the symbol shown on the pattern of a unique gift.
    
    https://core.telegram.org/bots/api#uniquegiftsymbol
    """
    name: str
    """Name of the symbol"""
    sticker: Sticker
    """The sticker that represents the unique gift"""
    rarity_per_mille: int
    """The number of unique gifts that receive this model for every 1000 gifts upgraded"""

class UniqueGiftBackdropColors(_Base, frozen=True):
    """This object describes the colors of the backdrop of a unique gift.
    
    https://core.telegram.org/bots/api#uniquegiftbackdropcolors
    """
    center_color: int
    """The color in the center of the backdrop in RGB format"""
    edge_color: int
    """The color on the edges of the backdrop in RGB format"""
    symbol_color: int
    """The color to be applied to the symbol in RGB format"""
    text_color: int
    """The color for the text on the backdrop in RGB format"""

class UniqueGiftBackdrop(_Base, frozen=True):
    """This object describes the backdrop of a unique gift.
    
    https://core.telegram.org/bots/api#uniquegiftbackdrop
    """
    name: str
    """Name of the backdrop"""
    colors: UniqueGiftBackdropColors
    """Colors of the backdrop"""
    rarity_per_mille: int
    """The number of unique gifts that receive this backdrop for every 1000 gifts upgraded"""

class UniqueGiftColors(_Base, frozen=True):
    """This object contains information about the color scheme for a user's name, message replies and link previews based on a unique gift.
    
    https://core.telegram.org/bots/api#uniquegiftcolors
    """
    model_custom_emoji_id: str
    """Custom emoji identifier of the unique gift's model"""
    symbol_custom_emoji_id: str
    """Custom emoji identifier of the unique gift's symbol"""
    light_theme_main_color: int
    """Main color used in light themes; RGB format"""
    light_theme_other_colors: List[int]
    """List of 1-3 additional colors used in light themes; RGB format"""
    dark_theme_main_color: int
    """Main color used in dark themes; RGB format"""
    dark_theme_other_colors: List[int]
    """List of 1-3 additional colors used in dark themes; RGB format"""

class UniqueGift(_Base, frozen=True):
    """This object describes a unique gift that was upgraded from a regular gift.
    
    https://core.telegram.org/bots/api#uniquegift
    """
    gift_id: str
    """Identifier of the regular gift from which the gift was upgraded"""
    base_name: str
    """Human-readable name of the regular gift from which this unique gift was upgraded"""
    name: str
    """Unique name of the gift. This name can be used in https://t.me/nft/... links and story areas."""
    number: int
    """Unique number of the upgraded gift among gifts upgraded from the same regular gift"""
    model: UniqueGiftModel
    """Model of the gift"""
    symbol: UniqueGiftSymbol
    """Symbol of the gift"""
    backdrop: UniqueGiftBackdrop
    """Backdrop of the gift"""
    is_premium: Optional[bool] = Field(default=None)
    """Optional. True, if the original regular gift was exclusively purchaseable by Telegram Premium subscribers"""
    is_burned: Optional[bool] = Field(default=None)
    """Optional. True, if the gift was used to craft another gift and isn't available anymore"""
    is_from_blockchain: Optional[bool] = Field(default=None)
    """Optional. True, if the gift is assigned from the TON blockchain and can't be resold or transferred in Telegram"""
    colors: Optional[UniqueGiftColors] = Field(default=None)
    """Optional. The color scheme that can be used by the gift's owner for the chat's name, replies to messages and link previews; for business account gifts and gifts that are currently on sale only"""
    publisher_chat: Optional[Chat] = Field(default=None)
    """Optional. Information about the chat that published the gift"""

class GiftInfo(_Base, frozen=True):
    """Describes a service message about a regular gift that was sent or received.
    
    https://core.telegram.org/bots/api#giftinfo
    """
    gift: Gift
    """Information about the gift"""
    owned_gift_id: Optional[str] = Field(default=None)
    """Optional. Unique identifier of the received gift for the bot; only present for gifts received on behalf of business accounts"""
    convert_star_count: Optional[int] = Field(default=None)
    """Optional. Number of Telegram Stars that can be claimed by the receiver by converting the gift; omitted if conversion to Telegram Stars is impossible"""
    prepaid_upgrade_star_count: Optional[int] = Field(default=None)
    """Optional. Number of Telegram Stars that were prepaid for the ability to upgrade the gift"""
    is_upgrade_separate: Optional[bool] = Field(default=None)
    """Optional. True, if the gift's upgrade was purchased after the gift was sent"""
    can_be_upgraded: Optional[bool] = Field(default=None)
    """Optional. True, if the gift can be upgraded to a unique gift"""
    text: Optional[str] = Field(default=None)
    """Optional. Text of the message that was added to the gift"""
    entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities that appear in the text"""
    is_private: Optional[bool] = Field(default=None)
    """Optional. True, if the sender and gift text are shown only to the gift receiver; otherwise, everyone will be able to see them"""
    unique_gift_number: Optional[int] = Field(default=None)
    """Optional. Unique number reserved for this gift when upgraded. See the number field in UniqueGift."""

class UniqueGiftInfo(_Base, frozen=True):
    """Describes a service message about a unique gift that was sent or received.
    
    https://core.telegram.org/bots/api#uniquegiftinfo
    """
    gift: UniqueGift
    """Information about the gift"""
    origin: str
    """Origin of the gift. Currently, either "upgrade" for gifts upgraded from regular gifts, "transfer" for gifts transferred from other users or channels, "resale" for gifts bought from other users, "gifted_upgrade" for upgrades purchased after the gift was sent, or "offer" for gifts bought or sold through gift purchase offers."""
    text: Optional[str] = Field(default=None)
    """Optional. Text of the message that was added to the gift"""
    entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities that appear in the text"""
    is_private: Optional[bool] = Field(default=None)
    """Optional. True, if the sender and gift text are shown only to the gift receiver; otherwise, everyone will be able to see them"""
    last_resale_currency: Optional[str] = Field(default=None)
    """Optional. For gifts bought from other users, the currency in which the payment for the gift was done. Currently, one of "XTR" for Telegram Stars or "TON" for TON grams."""
    last_resale_amount: Optional[int] = Field(default=None)
    """Optional. For gifts bought from other users, the price paid for the gift in either Telegram Stars or nanograms"""
    owned_gift_id: Optional[str] = Field(default=None)
    """Optional. Unique identifier of the received gift for the bot; only present for gifts received on behalf of business accounts"""
    transfer_star_count: Optional[int] = Field(default=None)
    """Optional. Number of Telegram Stars that must be paid to transfer the gift; omitted if the bot cannot transfer the gift"""
    next_transfer_date: Optional[int] = Field(default=None)
    """Optional. Point in time (Unix timestamp) when the gift can be transferred. If it is in the past, then the gift can be transferred now."""

class OwnedGiftRegular(_Base, frozen=True):
    """Describes a regular gift owned by a user or a chat.
    
    https://core.telegram.org/bots/api#ownedgiftregular
    """
    type: Literal["regular"] = Field(default='regular')
    """Type of the gift, always "regular" """
    gift: Gift
    """Information about the regular gift"""
    owned_gift_id: Optional[str] = Field(default=None)
    """Optional. Unique identifier of the gift for the bot; for gifts received on behalf of business accounts only"""
    sender_user: Optional[User] = Field(default=None)
    """Optional. Sender of the gift if it is a known user"""
    send_date: int
    """Date the gift was sent in Unix time"""
    text: Optional[str] = Field(default=None)
    """Optional. Text of the message that was added to the gift"""
    entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities that appear in the text"""
    is_private: Optional[bool] = Field(default=None)
    """Optional. True, if the sender and gift text are shown only to the gift receiver; otherwise, everyone will be able to see them"""
    is_saved: Optional[bool] = Field(default=None)
    """Optional. True, if the gift is displayed on the account's profile page; for gifts received on behalf of business accounts only"""
    can_be_upgraded: Optional[bool] = Field(default=None)
    """Optional. True, if the gift can be upgraded to a unique gift; for gifts received on behalf of business accounts only"""
    was_refunded: Optional[bool] = Field(default=None)
    """Optional. True, if the gift was refunded and isn't available anymore"""
    convert_star_count: Optional[int] = Field(default=None)
    """Optional. Number of Telegram Stars that can be claimed by the receiver instead of the gift; omitted if the gift cannot be converted to Telegram Stars; for gifts received on behalf of business accounts only"""
    prepaid_upgrade_star_count: Optional[int] = Field(default=None)
    """Optional. Number of Telegram Stars that were paid for the ability to upgrade the gift"""
    is_upgrade_separate: Optional[bool] = Field(default=None)
    """Optional. True, if the gift's upgrade was purchased after the gift was sent; for gifts received on behalf of business accounts only"""
    unique_gift_number: Optional[int] = Field(default=None)
    """Optional. Unique number reserved for this gift when upgraded. See the number field in UniqueGift."""

class OwnedGiftUnique(_Base, frozen=True):
    """Describes a unique gift received and owned by a user or a chat.
    
    https://core.telegram.org/bots/api#ownedgiftunique
    """
    type: Literal["unique"] = Field(default='unique')
    """Type of the gift, always "unique" """
    gift: UniqueGift
    """Information about the unique gift"""
    owned_gift_id: Optional[str] = Field(default=None)
    """Optional. Unique identifier of the received gift for the bot; for gifts received on behalf of business accounts only"""
    sender_user: Optional[User] = Field(default=None)
    """Optional. Sender of the gift if it is a known user"""
    send_date: int
    """Date the gift was sent in Unix time"""
    is_saved: Optional[bool] = Field(default=None)
    """Optional. True, if the gift is displayed on the account's profile page; for gifts received on behalf of business accounts only"""
    can_be_transferred: Optional[bool] = Field(default=None)
    """Optional. True, if the gift can be transferred to another owner; for gifts received on behalf of business accounts only"""
    transfer_star_count: Optional[int] = Field(default=None)
    """Optional. Number of Telegram Stars that must be paid to transfer the gift; omitted if the bot cannot transfer the gift"""
    next_transfer_date: Optional[int] = Field(default=None)
    """Optional. Point in time (Unix timestamp) when the gift can be transferred. If it is in the past, then the gift can be transferred now."""

class OwnedGifts(_Base, frozen=True):
    """Contains the list of gifts received and owned by a user or a chat.
    
    https://core.telegram.org/bots/api#ownedgifts
    """
    total_count: int
    """The total number of gifts owned by the user or the chat"""
    gifts: List[OwnedGift]
    """The list of gifts"""
    next_offset: Optional[str] = Field(default=None)
    """Optional. Offset for the next request. If empty, then there are no more results."""

class BotAccessSettings(_Base, frozen=True):
    """This object describes the access settings of a bot.
    
    https://core.telegram.org/bots/api#botaccesssettings
    """
    is_access_restricted: bool
    """True, if only selected users can access the bot. The bot's owner can always access it."""
    added_users: Optional[List[User]] = Field(default=None)
    """Optional. The list of other users who have access to the bot if the access is restricted"""

class AcceptedGiftTypes(_Base, frozen=True):
    """This object describes the types of gifts that can be gifted to a user or a chat.
    
    https://core.telegram.org/bots/api#acceptedgifttypes
    """
    unlimited_gifts: bool
    """True, if unlimited regular gifts are accepted"""
    limited_gifts: bool
    """True, if limited regular gifts are accepted"""
    unique_gifts: bool
    """True, if unique gifts or gifts that can be upgraded to unique for free are accepted"""
    premium_subscription: bool
    """True, if a Telegram Premium subscription is accepted"""
    gifts_from_channels: bool
    """True, if transfers of unique gifts from channels are accepted"""

class StarAmount(_Base, frozen=True):
    """Describes an amount of Telegram Stars.
    
    https://core.telegram.org/bots/api#staramount
    """
    amount: int
    """Integer amount of Telegram Stars, rounded to 0; can be negative"""
    nanostar_amount: Optional[int] = Field(default=None)
    """Optional. The number of 1/1000000000 shares of Telegram Stars; from -999999999 to 999999999; can be negative if and only if amount is non-positive"""

class BotCommand(_Base, frozen=True):
    """This object represents a bot command.
    
    https://core.telegram.org/bots/api#botcommand
    """
    command: str
    """Text of the command; 1-32 characters. Can contain only lowercase English letters, digits and underscores."""
    description: str
    """Description of the command; 1-256 characters"""
    is_ephemeral: Optional[bool] = Field(default=None)
    """Optional. True, if the command sends an ephemeral message, which can be seen only by the sender of the message and the bot"""

class BotCommandScopeDefault(_Base, frozen=True):
    """Represents the default scope of bot commands. Default commands are used if no commands with a narrower scope are specified for the user.
    
    https://core.telegram.org/bots/api#botcommandscopedefault
    """
    type: Literal["default"] = Field(default='default')
    """Scope type, must be default"""

class BotCommandScopeAllPrivateChats(_Base, frozen=True):
    """Represents the scope of bot commands, covering all private chats.
    
    https://core.telegram.org/bots/api#botcommandscopeallprivatechats
    """
    type: Literal["all_private_chats"] = Field(default='all_private_chats')
    """Scope type, must be all_private_chats"""

class BotCommandScopeAllGroupChats(_Base, frozen=True):
    """Represents the scope of bot commands, covering all group and supergroup chats.
    
    https://core.telegram.org/bots/api#botcommandscopeallgroupchats
    """
    type: Literal["all_group_chats"] = Field(default='all_group_chats')
    """Scope type, must be all_group_chats"""

class BotCommandScopeAllChatAdministrators(_Base, frozen=True):
    """Represents the scope of bot commands, covering all group and supergroup chat administrators.
    
    https://core.telegram.org/bots/api#botcommandscopeallchatadministrators
    """
    type: Literal["all_chat_administrators"] = Field(default='all_chat_administrators')
    """Scope type, must be all_chat_administrators"""

class BotCommandScopeChat(_Base, frozen=True):
    """Represents the scope of bot commands, covering a specific chat.
    
    https://core.telegram.org/bots/api#botcommandscopechat
    """
    type: Literal["chat"] = Field(default='chat')
    """Scope type, must be chat"""
    chat_id: Union[int, str]
    """Unique identifier for the target chat or username of the target supergroup in the format @username. Channel direct messages chats and channel chats aren't supported."""

class BotCommandScopeChatAdministrators(_Base, frozen=True):
    """Represents the scope of bot commands, covering all administrators of a specific group or supergroup chat.
    
    https://core.telegram.org/bots/api#botcommandscopechatadministrators
    """
    type: Literal["chat_administrators"] = Field(default='chat_administrators')
    """Scope type, must be chat_administrators"""
    chat_id: Union[int, str]
    """Unique identifier for the target chat or username of the target supergroup in the format @username. Channel direct messages chats and channel chats aren't supported."""

class BotCommandScopeChatMember(_Base, frozen=True):
    """Represents the scope of bot commands, covering a specific member of a group or supergroup chat.
    
    https://core.telegram.org/bots/api#botcommandscopechatmember
    """
    type: Literal["chat_member"] = Field(default='chat_member')
    """Scope type, must be chat_member"""
    chat_id: Union[int, str]
    """Unique identifier for the target chat or username of the target supergroup in the format @username. Channel direct messages chats and channel chats aren't supported."""
    user_id: int
    """Unique identifier of the target user"""

class BotName(_Base, frozen=True):
    """This object represents the bot's name.
    
    https://core.telegram.org/bots/api#botname
    """
    name: str
    """The bot's name"""

class BotDescription(_Base, frozen=True):
    """This object represents the bot's description.
    
    https://core.telegram.org/bots/api#botdescription
    """
    description: str
    """The bot's description"""

class BotShortDescription(_Base, frozen=True):
    """This object represents the bot's short description.
    
    https://core.telegram.org/bots/api#botshortdescription
    """
    short_description: str
    """The bot's short description"""

class MenuButtonCommands(_Base, frozen=True):
    """Represents a menu button, which opens the bot's list of commands.
    
    https://core.telegram.org/bots/api#menubuttoncommands
    """
    type: Literal["commands"] = Field(default='commands')
    """Type of the button, must be commands"""

class MenuButtonWebApp(_Base, frozen=True):
    """Represents a menu button, which launches a Web App.
    
    https://core.telegram.org/bots/api#menubuttonwebapp
    """
    type: Literal["web_app"] = Field(default='web_app')
    """Type of the button, must be web_app"""
    text: str
    """Text on the button"""
    web_app: WebAppInfo
    """Description of the Web App that will be launched when the user presses the button. The Web App will be able to send an arbitrary message on behalf of the user using the method answerWebAppQuery. Alternatively, a t.me link to a Web App of the bot can be specified in the object instead of the Web App's URL, in which case the Web App will be opened as if the user pressed the link."""

class MenuButtonDefault(_Base, frozen=True):
    """Describes that no specific value for the menu button was set.
    
    https://core.telegram.org/bots/api#menubuttondefault
    """
    type: Literal["default"] = Field(default='default')
    """Type of the button, must be default"""

class ChatBoostSourcePremium(_Base, frozen=True):
    """The boost was obtained by subscribing to Telegram Premium or by gifting a Telegram Premium subscription to another user.
    
    https://core.telegram.org/bots/api#chatboostsourcepremium
    """
    source: Literal["premium"] = Field(default='premium')
    """Source of the boost, always "premium" """
    user: User
    """User that boosted the chat"""

class ChatBoostSourceGiftCode(_Base, frozen=True):
    """The boost was obtained by the creation of Telegram Premium gift codes to boost a chat. Each such code boosts the chat 4 times for the duration of the corresponding Telegram Premium subscription.
    
    https://core.telegram.org/bots/api#chatboostsourcegiftcode
    """
    source: Literal["gift_code"] = Field(default='gift_code')
    """Source of the boost, always "gift_code" """
    user: User
    """User for which the gift code was created"""

class ChatBoostSourceGiveaway(_Base, frozen=True):
    """The boost was obtained by the creation of a Telegram Premium or a Telegram Star giveaway. This boosts the chat 4 times for the duration of the corresponding Telegram Premium subscription for Telegram Premium giveaways and prize_star_count / 500 times for one year for Telegram Star giveaways.
    
    https://core.telegram.org/bots/api#chatboostsourcegiveaway
    """
    source: Literal["giveaway"] = Field(default='giveaway')
    """Source of the boost, always "giveaway" """
    giveaway_message_id: int
    """Identifier of a message in the chat with the giveaway; the message could have been deleted already. May be 0 if the message isn't sent yet."""
    user: Optional[User] = Field(default=None)
    """Optional. User that won the prize in the giveaway if any; for Telegram Premium giveaways only"""
    prize_star_count: Optional[int] = Field(default=None)
    """Optional. The number of Telegram Stars to be split between giveaway winners; for Telegram Star giveaways only"""
    is_unclaimed: Optional[bool] = Field(default=None)
    """Optional. True, if the giveaway was completed, but there was no user to win the prize"""

class ChatBoost(_Base, frozen=True):
    """This object contains information about a chat boost.
    
    https://core.telegram.org/bots/api#chatboost
    """
    boost_id: str
    """Unique identifier of the boost"""
    add_date: int
    """Point in time (Unix timestamp) when the chat was boosted"""
    expiration_date: int
    """Point in time (Unix timestamp) when the boost will automatically expire, unless the booster's Telegram Premium subscription is prolonged"""
    source: ChatBoostSource
    """Source of the added boost"""

class ChatBoostUpdated(_Base, frozen=True):
    """This object represents a boost added to a chat or changed.
    
    https://core.telegram.org/bots/api#chatboostupdated
    """
    chat: Chat
    """Chat which was boosted"""
    boost: ChatBoost
    """Information about the chat boost"""

class ChatBoostRemoved(_Base, frozen=True):
    """This object represents a boost removed from a chat.
    
    https://core.telegram.org/bots/api#chatboostremoved
    """
    chat: Chat
    """Chat which was boosted"""
    boost_id: str
    """Unique identifier of the boost"""
    remove_date: int
    """Point in time (Unix timestamp) when the boost was removed"""
    source: ChatBoostSource
    """Source of the removed boost"""

class ChatOwnerLeft(_Base, frozen=True):
    """Describes a service message about the chat owner leaving the chat.
    
    https://core.telegram.org/bots/api#chatownerleft
    """
    new_owner: Optional[User] = Field(default=None)
    """Optional. The user who will become the new owner of the chat if the previous owner does not return to the chat"""

class ChatOwnerChanged(_Base, frozen=True):
    """Describes a service message about an ownership change in the chat.
    
    https://core.telegram.org/bots/api#chatownerchanged
    """
    new_owner: User
    """The new owner of the chat"""

class UserChatBoosts(_Base, frozen=True):
    """This object represents a list of boosts added to a chat by a user.
    
    https://core.telegram.org/bots/api#userchatboosts
    """
    boosts: List[ChatBoost]
    """The list of boosts added to the chat by the user"""

class BusinessBotRights(_Base, frozen=True):
    """Represents the rights of a business bot.
    
    https://core.telegram.org/bots/api#businessbotrights
    """
    can_reply: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can send and edit messages in the private chats that had incoming messages in the last 24 hours"""
    can_read_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can mark incoming private messages as read"""
    can_delete_sent_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can delete messages sent by the bot"""
    can_delete_all_messages: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can delete all private messages in managed chats"""
    can_edit_name: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can edit the first and last name of the business account"""
    can_edit_bio: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can edit the bio of the business account"""
    can_edit_profile_photo: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can edit the profile photo of the business account"""
    can_edit_username: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can edit the username of the business account"""
    can_change_gift_settings: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can change the privacy settings pertaining to gifts for the business account"""
    can_view_gifts_and_stars: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can view gifts and the amount of Telegram Stars owned by the business account"""
    can_convert_gifts_to_stars: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can convert regular gifts owned by the business account to Telegram Stars"""
    can_transfer_and_upgrade_gifts: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can transfer and upgrade gifts owned by the business account"""
    can_transfer_stars: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can transfer Telegram Stars received by the business account to its own account, or use them to upgrade and transfer gifts"""
    can_manage_stories: Optional[bool] = Field(default=None)
    """Optional. True, if the bot can post, edit and delete stories on behalf of the business account"""

class BusinessConnection(_Base, frozen=True):
    """Describes the connection of the bot with a business account.
    
    https://core.telegram.org/bots/api#businessconnection
    """
    id: str
    """Unique identifier of the business connection"""
    user: User
    """Business account user that created the business connection"""
    user_chat_id: int
    """Identifier of a private chat with the user who created the business connection. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier."""
    date: int
    """Date the connection was established in Unix time"""
    rights: Optional[BusinessBotRights] = Field(default=None)
    """Optional. Rights of the business bot"""
    is_enabled: bool
    """True, if the connection is active"""

class BusinessMessagesDeleted(_Base, frozen=True):
    """This object is received when messages are deleted from a connected business account.
    
    https://core.telegram.org/bots/api#businessmessagesdeleted
    """
    business_connection_id: str
    """Unique identifier of the business connection"""
    chat: Chat
    """Information about a chat in the business account. The bot may not have access to the chat or the corresponding user."""
    message_ids: List[int]
    """The list of identifiers of deleted messages in the chat of the business account"""

class SentWebAppMessage(_Base, frozen=True):
    """Describes an inline message sent by a Web App on behalf of a user.
    
    https://core.telegram.org/bots/api#sentwebappmessage
    """
    inline_message_id: Optional[str] = Field(default=None)
    """Optional. Identifier of the sent inline message. Available only if there is an inline keyboard attached to the message."""

class SentGuestMessage(_Base, frozen=True):
    """Describes an inline message sent by a guest bot.
    
    https://core.telegram.org/bots/api#sentguestmessage
    """
    inline_message_id: str
    """Identifier of the sent inline message"""

class PreparedInlineMessage(_Base, frozen=True):
    """Describes an inline message to be sent by a user of a Mini App.
    
    https://core.telegram.org/bots/api#preparedinlinemessage
    """
    id: str
    """Unique identifier of the prepared message"""
    expiration_date: int
    """Expiration date of the prepared message, in Unix time. Expired prepared messages can no longer be used."""

class PreparedKeyboardButton(_Base, frozen=True):
    """Describes a keyboard button to be used by a user of a Mini App.
    
    https://core.telegram.org/bots/api#preparedkeyboardbutton
    """
    id: str
    """Unique identifier of the keyboard button"""

class ResponseParameters(_Base, frozen=True):
    """Describes why a request was unsuccessful.
    
    https://core.telegram.org/bots/api#responseparameters
    """
    migrate_to_chat_id: Optional[int] = Field(default=None)
    """Optional. The group has been migrated to a supergroup with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier."""
    retry_after: Optional[int] = Field(default=None)
    """Optional. In case of exceeding flood control, the number of seconds left to wait before the request can be repeated"""

class InputMediaAnimation(_Base, frozen=True):
    """Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent.
    
    https://core.telegram.org/bots/api#inputmediaanimation
    """
    type: Literal["animation"] = Field(default='animation')
    """Type of the media, must be animation"""
    media: str
    """File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    thumbnail: Optional[str] = Field(default=None)
    """Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the animation to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the animation caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    width: Optional[int] = Field(default=None)
    """Optional. Animation width"""
    height: Optional[int] = Field(default=None)
    """Optional. Animation height"""
    duration: Optional[int] = Field(default=None)
    """Optional. Animation duration in seconds"""
    has_spoiler: Optional[bool] = Field(default=None)
    """Optional. Pass True if the animation needs to be covered with a spoiler animation"""

class InputMediaAudio(_Base, frozen=True):
    """Represents an audio file to be treated as music to be sent.
    
    https://core.telegram.org/bots/api#inputmediaaudio
    """
    type: Literal["audio"] = Field(default='audio')
    """Type of the media, must be audio"""
    media: str
    """File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    thumbnail: Optional[str] = Field(default=None)
    """Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the audio to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the audio caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    duration: Optional[int] = Field(default=None)
    """Optional. Duration of the audio in seconds"""
    performer: Optional[str] = Field(default=None)
    """Optional. Performer of the audio"""
    title: Optional[str] = Field(default=None)
    """Optional. Title of the audio"""

class InputMediaDocument(_Base, frozen=True):
    """Represents a general file to be sent.
    
    https://core.telegram.org/bots/api#inputmediadocument
    """
    type: Literal["document"] = Field(default='document')
    """Type of the media, must be document"""
    media: str
    """File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    thumbnail: Optional[str] = Field(default=None)
    """Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the document to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the document caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    disable_content_type_detection: Optional[bool] = Field(default=None)
    """Optional. Disables automatic server-side content type detection for files uploaded using multipart/form-data. Always True, if the document is sent as part of an album."""

class InputMediaLink(_Base, frozen=True):
    """Represents an HTTP link to be sent.
    
    https://core.telegram.org/bots/api#inputmedialink
    """
    type: Literal["link"] = Field(default='link')
    """Type of the media, must be link"""
    url: str
    """HTTP URL of the link"""

class InputMediaLivePhoto(_Base, frozen=True):
    """Represents a live photo to be sent.
    
    https://core.telegram.org/bots/api#inputmedialivephoto
    """
    type: Literal["live_photo"] = Field(default='live_photo')
    """Type of the media, must be live_photo"""
    media: str
    """Video of the live photo to send. Pass a file_id to send a file that exists on the Telegram servers (recommended) or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Sending live photos by a URL is currently unsupported."""
    photo: str
    """The static photo to send. Pass a file_id to send a file that exists on the Telegram servers (recommended) or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Sending live photos by a URL is currently unsupported."""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the live photo to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the live photo caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    has_spoiler: Optional[bool] = Field(default=None)
    """Optional. Pass True if the live photo needs to be covered with a spoiler animation"""

class InputMediaLocation(_Base, frozen=True):
    """Represents a location to be sent.
    
    https://core.telegram.org/bots/api#inputmedialocation
    """
    type: Literal["location"] = Field(default='location')
    """Type of the media, must be location"""
    latitude: float
    """Latitude of the location"""
    longitude: float
    """Longitude of the location"""
    horizontal_accuracy: Optional[float] = Field(default=None)
    """Optional. The radius of uncertainty for the location, measured in meters; 0-1500"""

class InputMediaPhoto(_Base, frozen=True):
    """Represents a photo to be sent.
    
    https://core.telegram.org/bots/api#inputmediaphoto
    """
    type: Literal["photo"] = Field(default='photo')
    """Type of the media, must be photo"""
    media: str
    """File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the photo caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    has_spoiler: Optional[bool] = Field(default=None)
    """Optional. Pass True if the photo needs to be covered with a spoiler animation"""

class InputMediaSticker(_Base, frozen=True):
    """Represents a sticker file to be sent.
    
    https://core.telegram.org/bots/api#inputmediasticker
    """
    type: Literal["sticker"] = Field(default='sticker')
    """Type of the media, must be sticker"""
    media: str
    """File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a .WEBP sticker from the Internet, or pass "attach://<file_attach_name>" to upload a new .WEBP, .TGS, or .WEBM sticker using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    emoji: Optional[str] = Field(default=None)
    """Optional. Emoji associated with the sticker; only for just uploaded stickers"""

class InputMediaVenue(_Base, frozen=True):
    """Represents a venue to be sent.
    
    https://core.telegram.org/bots/api#inputmediavenue
    """
    type: Literal["venue"] = Field(default='venue')
    """Type of the media, must be venue"""
    latitude: float
    """Latitude of the location"""
    longitude: float
    """Longitude of the location"""
    title: str
    """Name of the venue"""
    address: str
    """Address of the venue"""
    foursquare_id: Optional[str] = Field(default=None)
    """Optional. Foursquare identifier of the venue"""
    foursquare_type: Optional[str] = Field(default=None)
    """Optional. Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)"""
    google_place_id: Optional[str] = Field(default=None)
    """Optional. Google Places identifier of the venue"""
    google_place_type: Optional[str] = Field(default=None)
    """Optional. Google Places type of the venue. (See supported types.)"""

class InputMediaVideo(_Base, frozen=True):
    """Represents a video to be sent.
    
    https://core.telegram.org/bots/api#inputmediavideo
    """
    type: Literal["video"] = Field(default='video')
    """Type of the media, must be video"""
    media: str
    """File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    thumbnail: Optional[str] = Field(default=None)
    """Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    cover: Optional[str] = Field(default=None)
    """Optional. Cover for the video in the message. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    start_timestamp: Optional[int] = Field(default=None)
    """Optional. Start timestamp for the video in the message"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the video to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the video caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    width: Optional[int] = Field(default=None)
    """Optional. Video width"""
    height: Optional[int] = Field(default=None)
    """Optional. Video height"""
    duration: Optional[int] = Field(default=None)
    """Optional. Video duration in seconds"""
    supports_streaming: Optional[bool] = Field(default=None)
    """Optional. Pass True if the uploaded video is suitable for streaming"""
    has_spoiler: Optional[bool] = Field(default=None)
    """Optional. Pass True if the video needs to be covered with a spoiler animation"""

class InputMediaVoiceNote(_Base, frozen=True):
    """Represents a voice message file to be sent.
    
    https://core.telegram.org/bots/api#inputmediavoicenote
    """
    type: Literal["voice_note"] = Field(default='voice_note')
    """Type of the media, must be voice_note"""
    media: str
    """File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the voice message to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the voice message caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    duration: Optional[int] = Field(default=None)
    """Optional. Duration of the voice message in seconds"""

class InputPaidMediaLivePhoto(_Base, frozen=True):
    """The paid media to send is a live photo.
    
    https://core.telegram.org/bots/api#inputpaidmedialivephoto
    """
    type: Literal["live_photo"] = Field(default='live_photo')
    """Type of the media, must be live_photo"""
    media: str
    """Video of the live photo to send. Pass a file_id to send a file that exists on the Telegram servers (recommended) or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Sending live photos by a URL is currently unsupported."""
    photo: str
    """The static photo to send. Pass a file_id to send a file that exists on the Telegram servers (recommended) or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Sending live photos by a URL is currently unsupported."""

class InputPaidMediaPhoto(_Base, frozen=True):
    """The paid media to send is a photo.
    
    https://core.telegram.org/bots/api#inputpaidmediaphoto
    """
    type: Literal["photo"] = Field(default='photo')
    """Type of the media, must be photo"""
    media: str
    """File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""

class InputPaidMediaVideo(_Base, frozen=True):
    """The paid media to send is a video.
    
    https://core.telegram.org/bots/api#inputpaidmediavideo
    """
    type: Literal["video"] = Field(default='video')
    """Type of the media, must be video"""
    media: str
    """File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    thumbnail: Optional[str] = Field(default=None)
    """Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    cover: Optional[str] = Field(default=None)
    """Optional. Cover for the video in the message. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    start_timestamp: Optional[int] = Field(default=None)
    """Optional. Start timestamp for the video in the message"""
    width: Optional[int] = Field(default=None)
    """Optional. Video width"""
    height: Optional[int] = Field(default=None)
    """Optional. Video height"""
    duration: Optional[int] = Field(default=None)
    """Optional. Video duration in seconds"""
    supports_streaming: Optional[bool] = Field(default=None)
    """Optional. Pass True if the uploaded video is suitable for streaming"""

class InputProfilePhotoStatic(_Base, frozen=True):
    """A static profile photo in the .JPG format.
    
    https://core.telegram.org/bots/api#inputprofilephotostatic
    """
    type: Literal["static"] = Field(default='static')
    """Type of the profile photo, must be static"""
    photo: str
    """The static profile photo. Profile photos can't be reused and can only be uploaded as a new file, so you can pass "attach://<file_attach_name>" if the photo was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""

class InputProfilePhotoAnimated(_Base, frozen=True):
    """An animated profile photo in the MPEG4 format.
    
    https://core.telegram.org/bots/api#inputprofilephotoanimated
    """
    type: Literal["animated"] = Field(default='animated')
    """Type of the profile photo, must be animated"""
    animation: str
    """The animated profile photo. Profile photos can't be reused and can only be uploaded as a new file, so you can pass "attach://<file_attach_name>" if the photo was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    main_frame_timestamp: Optional[float] = Field(default=None)
    """Optional. Timestamp in seconds of the frame that will be used as the static profile photo. Defaults to 0.0."""

class InputStoryContentPhoto(_Base, frozen=True):
    """Describes a photo to post as a story.
    
    https://core.telegram.org/bots/api#inputstorycontentphoto
    """
    type: Literal["photo"] = Field(default='photo')
    """Type of the content, must be photo"""
    photo: str
    """The photo to post as a story. The photo must be of the size 1080x1920 and must not exceed 10 MB. The photo can't be reused and can only be uploaded as a new file, so you can pass "attach://<file_attach_name>" if the photo was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""

class InputStoryContentVideo(_Base, frozen=True):
    """Describes a video to post as a story.
    
    https://core.telegram.org/bots/api#inputstorycontentvideo
    """
    type: Literal["video"] = Field(default='video')
    """Type of the content, must be video"""
    video: str
    """The video to post as a story. The video must be of the size 720x1280, streamable, encoded with H.265 codec, with key frames added each second in the MPEG4 format, and must not exceed 30 MB. The video can't be reused and can only be uploaded as a new file, so you can pass "attach://<file_attach_name>" if the video was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    duration: Optional[float] = Field(default=None)
    """Optional. Precise duration of the video in seconds; 0-60"""
    cover_frame_timestamp: Optional[float] = Field(default=None)
    """Optional. Timestamp in seconds of the frame that will be used as the static cover for the story. Defaults to 0.0."""
    is_animation: Optional[bool] = Field(default=None)
    """Optional. Pass True if the video has no sound"""

class Sticker(_Base, frozen=True):
    """This object represents a sticker.
    
    https://core.telegram.org/bots/api#sticker
    """
    file_id: str
    """Identifier for this file, which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    type: str
    """Type of the sticker, currently one of "regular", "mask", "custom_emoji". The type of the sticker is independent from its format, which is determined by the fields is_animated and is_video."""
    width: int
    """Sticker width"""
    height: int
    """Sticker height"""
    is_animated: bool
    """True, if the sticker is animated"""
    is_video: bool
    """True, if the sticker is a video sticker"""
    thumbnail: Optional[PhotoSize] = Field(default=None)
    """Optional. Sticker thumbnail in the .WEBP or .JPG format"""
    emoji: Optional[str] = Field(default=None)
    """Optional. Emoji associated with the sticker"""
    set_name: Optional[str] = Field(default=None)
    """Optional. Name of the sticker set to which the sticker belongs"""
    premium_animation: Optional[File] = Field(default=None)
    """Optional. For premium regular stickers, premium animation for the sticker"""
    mask_position: Optional[MaskPosition] = Field(default=None)
    """Optional. For mask stickers, the position where the mask should be placed"""
    custom_emoji_id: Optional[str] = Field(default=None)
    """Optional. For custom emoji stickers, unique identifier of the custom emoji"""
    needs_repainting: Optional[bool] = Field(default=None)
    """Optional. True, if the sticker must be repainted to a text color in messages, the color of the Telegram Premium badge in emoji status, white color on chat photos, or another appropriate color in other places"""
    file_size: Optional[int] = Field(default=None)
    """Optional. File size in bytes"""

class StickerSet(_Base, frozen=True):
    """This object represents a sticker set.
    
    https://core.telegram.org/bots/api#stickerset
    """
    name: str
    """Sticker set name"""
    title: str
    """Sticker set title"""
    sticker_type: str
    """Type of stickers in the set, currently one of "regular", "mask", "custom_emoji" """
    stickers: List[Sticker]
    """List of all set stickers"""
    thumbnail: Optional[PhotoSize] = Field(default=None)
    """Optional. Sticker set thumbnail in the .WEBP, .TGS, or .WEBM format"""

class MaskPosition(_Base, frozen=True):
    """This object describes the position on faces where a mask should be placed by default.
    
    https://core.telegram.org/bots/api#maskposition
    """
    point: str
    """The part of the face relative to which the mask should be placed. One of "forehead", "eyes", "mouth", or "chin"."""
    x_shift: float
    """Shift by X-axis measured in widths of the mask scaled to the face size, from left to right. For example, choosing -1.0 will place mask just to the left of the default mask position."""
    y_shift: float
    """Shift by Y-axis measured in heights of the mask scaled to the face size, from top to bottom. For example, 1.0 will place the mask just below the default mask position."""
    scale: float
    """Mask scaling coefficient. For example, 2.0 means double size."""

class InputSticker(_Base, frozen=True):
    """This object describes a sticker to be added to a sticker set.
    
    https://core.telegram.org/bots/api#inputsticker
    """
    sticker: str
    """The added sticker. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new file using multipart/form-data under <file_attach_name> name. Animated and video stickers can't be uploaded via HTTP URL. More information on Sending Files: https://core.telegram.org/bots/api#sending-files"""
    format: str
    """Format of the added sticker, must be one of "static" for a .WEBP or .PNG image, "animated" for a .TGS animation, "video" for a .WEBM video"""
    emoji_list: List[str]
    """List of 1-20 emoji associated with the sticker"""
    mask_position: Optional[MaskPosition] = Field(default=None)
    """Optional. Position where the mask should be placed on faces. For "mask" stickers only."""
    keywords: Optional[List[str]] = Field(default=None)
    """Optional. List of 0-20 search keywords for the sticker with total length of up to 64 characters. For "regular" and "custom_emoji" stickers only."""

class RichMessage(_Base, frozen=True):
    """Rich formatted message.
    
    https://core.telegram.org/bots/api#richmessage
    """
    blocks: List[RichBlock]
    """Content of the message"""
    is_rtl: Optional[bool] = Field(default=None)
    """Optional. True, if the rich message must be shown right-to-left"""

class InputRichMessage(_Base, frozen=True):
    """Describes a rich message to be sent. Exactly one of the fields html, markdown, or blocks must be used.
    
    https://core.telegram.org/bots/api#inputrichmessage
    """
    blocks: Optional[List[InputRichBlock]] = Field(default=None)
    """Optional. Content of the rich message to send described as a list of blocks"""
    html: Optional[str] = Field(default=None)
    """Optional. Content of the rich message to send described using HTML formatting. See rich message formatting options for more details. Use media field to specify the media used in the message."""
    markdown: Optional[str] = Field(default=None)
    """Optional. Content of the rich message to send described using Markdown formatting. See rich message formatting options for more details. Use media field to specify the media used in the message."""
    media: Optional[List[InputRichMessageMedia]] = Field(default=None)
    """Optional. List of media that are specified in the markdown or html fields using tg://photo?id=, tg://video?id=, tg://document?id=, and tg://audio?id= links"""
    is_rtl: Optional[bool] = Field(default=None)
    """Optional. Pass True if the rich message must be shown right-to-left"""
    skip_entity_detection: Optional[bool] = Field(default=None)
    """Optional. Pass True to skip automatic detection of entities (e.g., URLs, email addresses, username mentions, hashtags, cashtags, bot commands, or phone numbers) in the text"""

class InputRichMessageMedia(_Base, frozen=True):
    """Describes a media element embedded in an outgoing rich message.
    
    https://core.telegram.org/bots/api#inputrichmessagemedia
    """
    id: str
    """Unique identifier of the media used in a tg://photo?id=, tg://video?id=, tg://document?id=, or tg://audio?id= link. 1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed."""
    media: Union[InputMediaAnimation, InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo, InputMediaVoiceNote]
    """The media to be sent. Everything except the media itself and its properties is ignored."""

class RichMessageButton(_Base, frozen=True):
    """This object represents a button in a RichMessage. Exactly one of the fields other than text and style must be used to specify the type of the button.
    
    https://core.telegram.org/bots/api#richmessagebutton
    """
    text: RichText
    """Text of the button. May contain only plain text, RichTextCustomEmoji and RichTextDateTime entities."""
    style: Optional[str] = Field(default=None)
    """Optional. Style of the button. Must be one of "danger", "success", "primary", or "link" (the button is shown as a regular link without borders). Apps may use theme-specific colors for the button background and text based on the style. The style "link" is allowed only for callback buttons."""
    url: Optional[str] = Field(default=None)
    """Optional. HTTP or tg:// URL to be opened when the button is pressed. Links tg://user?id=<user_id> can be used to mention a user by their identifier without using a username, if this is allowed by their privacy settings."""
    callback_data: Optional[str] = Field(default=None)
    """Optional. Data to be sent in a callback query to the bot when the button is pressed, 1-64 bytes"""
    web_app: Optional[WebAppInfo] = Field(default=None)
    """Optional. Description of the Web App that will be launched when the user presses the button. The Web App will be able to send an arbitrary message on behalf of the user using the method answerWebAppQuery. Available only in private chats between a user and the bot. Not supported for messages sent on behalf of a business account."""
    login_url: Optional[LoginUrl] = Field(default=None)
    """Optional. An HTTPS URL used to automatically authorize the user. Can be used as a replacement for the Telegram Login Widget. Not supported for ephemeral messages."""
    switch_inline_query: Optional[str] = Field(default=None)
    """Optional. If set, pressing the button will prompt the user to select one of their chats, open that chat and insert the bot's username and the specified inline query in the input field. May be empty, in which case just the bot's username will be inserted. Not supported for messages sent in channel direct messages chats and on behalf of a business account."""
    switch_inline_query_current_chat: Optional[str] = Field(default=None)
    """Optional. If set, pressing the button will insert the bot's username and the specified inline query in the current chat's input field. May be empty, in which case only the bot's username will be inserted. Not supported in channels and for messages sent in channel direct messages chats and on behalf of a business account."""
    switch_inline_query_chosen_chat: Optional[SwitchInlineQueryChosenChat] = Field(default=None)
    """Optional. If set, pressing the button will prompt the user to select one of their chats of the specified type, open that chat and insert the bot's username and the specified inline query in the input field. Not supported for messages sent in channel direct messages chats and on behalf of a business account."""
    copy_text: Optional[CopyTextButton] = Field(default=None)
    """Optional. A button that copies the specified text to the clipboard"""
    disabled: Optional[DisabledButton] = Field(default=None)
    """Optional. If set, then the button is disabled and does nothing"""

class RichTextBold(_Base, frozen=True):
    """A bold text.
    
    https://core.telegram.org/bots/api#richtextbold
    """
    type: Literal["bold"] = Field(default='bold')
    """Type of the rich text, always "bold" """
    text: RichText
    """The text"""

class RichTextItalic(_Base, frozen=True):
    """An italicized text.
    
    https://core.telegram.org/bots/api#richtextitalic
    """
    type: Literal["italic"] = Field(default='italic')
    """Type of the rich text, always "italic" """
    text: RichText
    """The text"""

class RichTextUnderline(_Base, frozen=True):
    """An underlined text.
    
    https://core.telegram.org/bots/api#richtextunderline
    """
    type: Literal["underline"] = Field(default='underline')
    """Type of the rich text, always "underline" """
    text: RichText
    """The text"""

class RichTextStrikethrough(_Base, frozen=True):
    """A strikethrough text.
    
    https://core.telegram.org/bots/api#richtextstrikethrough
    """
    type: Literal["strikethrough"] = Field(default='strikethrough')
    """Type of the rich text, always "strikethrough" """
    text: RichText
    """The text"""

class RichTextSpoiler(_Base, frozen=True):
    """A text covered by a spoiler.
    
    https://core.telegram.org/bots/api#richtextspoiler
    """
    type: Literal["spoiler"] = Field(default='spoiler')
    """Type of the rich text, always "spoiler" """
    text: RichText
    """The text"""

class RichTextDateTime(_Base, frozen=True):
    """Formatted date and time.
    
    https://core.telegram.org/bots/api#richtextdatetime
    """
    type: Literal["date_time"] = Field(default='date_time')
    """Type of the rich text, always "date_time" """
    text: RichText
    """The text"""
    unix_time: int
    """The Unix time associated with the entity"""
    date_time_format: str
    """The string that defines the formatting of the date and time. See date-time entity formatting for more details."""

class RichTextTextMention(_Base, frozen=True):
    """A mention of a Telegram user by their identifier.
    
    https://core.telegram.org/bots/api#richtexttextmention
    """
    type: Literal["text_mention"] = Field(default='text_mention')
    """Type of the rich text, always "text_mention" """
    text: RichText
    """The text"""
    user: User
    """The mentioned user"""

class RichTextSubscript(_Base, frozen=True):
    """A subscript text.
    
    https://core.telegram.org/bots/api#richtextsubscript
    """
    type: Literal["subscript"] = Field(default='subscript')
    """Type of the rich text, always "subscript" """
    text: RichText
    """The text"""

class RichTextSuperscript(_Base, frozen=True):
    """A superscript text.
    
    https://core.telegram.org/bots/api#richtextsuperscript
    """
    type: Literal["superscript"] = Field(default='superscript')
    """Type of the rich text, always "superscript" """
    text: RichText
    """The text"""

class RichTextMarked(_Base, frozen=True):
    """A marked text.
    
    https://core.telegram.org/bots/api#richtextmarked
    """
    type: Literal["marked"] = Field(default='marked')
    """Type of the rich text, always "marked" """
    text: RichText
    """The text"""

class RichTextCode(_Base, frozen=True):
    """A monowidth text.
    
    https://core.telegram.org/bots/api#richtextcode
    """
    type: Literal["code"] = Field(default='code')
    """Type of the rich text, always "code" """
    text: RichText
    """The text"""

class RichTextCustomEmoji(_Base, frozen=True):
    """A custom emoji.
    
    https://core.telegram.org/bots/api#richtextcustomemoji
    """
    type: Literal["custom_emoji"] = Field(default='custom_emoji')
    """Type of the rich text, always "custom_emoji" """
    custom_emoji_id: str
    """Unique identifier of the custom emoji. Use getCustomEmojiStickers to get full information about the sticker."""
    alternative_text: str
    """Alternative emoji for the custom emoji"""

class RichTextMathematicalExpression(_Base, frozen=True):
    """A mathematical expression.
    
    https://core.telegram.org/bots/api#richtextmathematicalexpression
    """
    type: Literal["mathematical_expression"] = Field(default='mathematical_expression')
    """Type of the rich text, always "mathematical_expression" """
    expression: str
    """The expression in LaTeX format"""

class RichTextUrl(_Base, frozen=True):
    """A text with a link.
    
    https://core.telegram.org/bots/api#richtexturl
    """
    type: Literal["url"] = Field(default='url')
    """Type of the rich text, always "url" """
    text: RichText
    """The text"""
    url: str
    """URL of the link"""

class RichTextEmailAddress(_Base, frozen=True):
    """A text with an email address.
    
    https://core.telegram.org/bots/api#richtextemailaddress
    """
    type: Literal["email_address"] = Field(default='email_address')
    """Type of the rich text, always "email_address" """
    text: RichText
    """The text"""
    email_address: str
    """The email address"""

class RichTextPhoneNumber(_Base, frozen=True):
    """A text with a phone number.
    
    https://core.telegram.org/bots/api#richtextphonenumber
    """
    type: Literal["phone_number"] = Field(default='phone_number')
    """Type of the rich text, always "phone_number" """
    text: RichText
    """The text"""
    phone_number: str
    """The phone number"""

class RichTextBankCardNumber(_Base, frozen=True):
    """A text with a bank card number.
    
    https://core.telegram.org/bots/api#richtextbankcardnumber
    """
    type: Literal["bank_card_number"] = Field(default='bank_card_number')
    """Type of the rich text, always "bank_card_number" """
    text: RichText
    """The text"""
    bank_card_number: str
    """The bank card number"""

class RichTextMention(_Base, frozen=True):
    """A mention by a username.
    
    https://core.telegram.org/bots/api#richtextmention
    """
    type: Literal["mention"] = Field(default='mention')
    """Type of the rich text, always "mention" """
    text: RichText
    """The text"""
    username: str
    """The username"""

class RichTextHashtag(_Base, frozen=True):
    """A hashtag.
    
    https://core.telegram.org/bots/api#richtexthashtag
    """
    type: Literal["hashtag"] = Field(default='hashtag')
    """Type of the rich text, always "hashtag" """
    text: RichText
    """The text"""
    hashtag: str
    """The hashtag"""

class RichTextCashtag(_Base, frozen=True):
    """A cashtag.
    
    https://core.telegram.org/bots/api#richtextcashtag
    """
    type: Literal["cashtag"] = Field(default='cashtag')
    """Type of the rich text, always "cashtag" """
    text: RichText
    """The text"""
    cashtag: str
    """The cashtag"""

class RichTextBotCommand(_Base, frozen=True):
    """A bot command.
    
    https://core.telegram.org/bots/api#richtextbotcommand
    """
    type: Literal["bot_command"] = Field(default='bot_command')
    """Type of the rich text, always "bot_command" """
    text: RichText
    """The text"""
    bot_command: str
    """The bot command"""

class RichTextButton(_Base, frozen=True):
    """A button.
    
    https://core.telegram.org/bots/api#richtextbutton
    """
    type: Literal["button"] = Field(default='button')
    """Type of the rich text, always "button" """
    button: RichMessageButton
    """The button"""

class RichTextAnchor(_Base, frozen=True):
    """An anchor.
    
    https://core.telegram.org/bots/api#richtextanchor
    """
    type: Literal["anchor"] = Field(default='anchor')
    """Type of the rich text, always "anchor" """
    name: str
    """The name of the anchor"""

class RichTextAnchorLink(_Base, frozen=True):
    """A link to an anchor.
    
    https://core.telegram.org/bots/api#richtextanchorlink
    """
    type: Literal["anchor_link"] = Field(default='anchor_link')
    """Type of the rich text, always "anchor_link" """
    text: RichText
    """The link text"""
    anchor_name: str
    """The name of the anchor. If the name is empty, then the link brings back to the top of the message."""

class RichTextReference(_Base, frozen=True):
    """A reference.
    
    https://core.telegram.org/bots/api#richtextreference
    """
    type: Literal["reference"] = Field(default='reference')
    """Type of the rich text, always "reference" """
    text: RichText
    """Text of the reference"""
    name: str
    """The name of the reference"""

class RichTextReferenceLink(_Base, frozen=True):
    """A link to a reference.
    
    https://core.telegram.org/bots/api#richtextreferencelink
    """
    type: Literal["reference_link"] = Field(default='reference_link')
    """Type of the rich text, always "reference_link" """
    text: RichText
    """The link text"""
    reference_name: str
    """The name of the reference"""

class RichBlockCaption(_Base, frozen=True):
    """Caption of a rich formatted block.
    
    https://core.telegram.org/bots/api#richblockcaption
    """
    text: RichText
    """Block caption"""
    credit: Optional[RichText] = Field(default=None)
    """Optional. Block credit which corresponds to the HTML tag <cite>"""

class RichBlockTableCell(_Base, frozen=True):
    """Cell in a table.
    
    https://core.telegram.org/bots/api#richblocktablecell
    """
    text: Optional[RichText] = Field(default=None)
    """Optional. Text in the cell. If omitted, then the cell is invisible."""
    is_header: Optional[bool] = Field(default=None)
    """Optional. True, if the cell is a header cell"""
    colspan: Optional[int] = Field(default=None)
    """Optional. The number of columns the cell spans if it is bigger than 1"""
    rowspan: Optional[int] = Field(default=None)
    """Optional. The number of rows the cell spans if it is bigger than 1"""
    align: str
    """Horizontal cell content alignment. Currently, must be one of "left", "center", or "right"."""
    valign: str
    """Vertical cell content alignment. Currently, must be one of "top", "middle", or "bottom"."""

class RichBlockListItem(_Base, frozen=True):
    """An item of a list.
    
    https://core.telegram.org/bots/api#richblocklistitem
    """
    label: str
    """Label of the item"""
    blocks: List[RichBlock]
    """The content of the item"""
    has_checkbox: Optional[bool] = Field(default=None)
    """Optional. True, if the item has a checkbox"""
    is_checked: Optional[bool] = Field(default=None)
    """Optional. True, if the item has a checked checkbox"""
    value: Optional[int] = Field(default=None)
    """Optional. For ordered lists, the numeric value of the item label"""
    type: Optional[str] = Field(default=None)
    """Optional. For ordered lists, the type of the item label; must be one of "a" for lowercase letters, "A" for uppercase letters, "i" for lowercase Roman numerals, "I" for uppercase Roman numerals, or "1" for decimal numbers"""

class RichBlockParagraph(_Base, frozen=True):
    """A text paragraph, corresponding to the HTML tag <p>.
    
    https://core.telegram.org/bots/api#richblockparagraph
    """
    type: Literal["paragraph"] = Field(default='paragraph')
    """Type of the block, always "paragraph" """
    text: RichText
    """Text of the block"""

class RichBlockSectionHeading(_Base, frozen=True):
    """A section heading, corresponding to the HTML tags <h1>, <h2>, <h3>, <h4>, <h5>, or <h6>.
    
    https://core.telegram.org/bots/api#richblocksectionheading
    """
    type: Literal["heading"] = Field(default='heading')
    """Type of the block, always "heading" """
    text: RichText
    """Text of the block"""
    size: int
    """Relative size of the text font; 1-6, 1 is the largest, 6 is the smallest"""

class RichBlockPreformatted(_Base, frozen=True):
    """A preformatted text block, corresponding to the nested HTML tags <pre> and <code>.
    
    https://core.telegram.org/bots/api#richblockpreformatted
    """
    type: Literal["pre"] = Field(default='pre')
    """Type of the block, always "pre" """
    text: RichText
    """Text of the block"""
    language: Optional[str] = Field(default=None)
    """Optional. The programming language of the text"""

class RichBlockFooter(_Base, frozen=True):
    """A footer, corresponding to the HTML tag <footer>.
    
    https://core.telegram.org/bots/api#richblockfooter
    """
    type: Literal["footer"] = Field(default='footer')
    """Type of the block, always "footer" """
    text: RichText
    """Text of the block"""

class RichBlockDivider(_Base, frozen=True):
    """A divider, corresponding to the HTML tag <hr/>.
    
    https://core.telegram.org/bots/api#richblockdivider
    """
    type: Literal["divider"] = Field(default='divider')
    """Type of the block, always "divider" """

class RichBlockMathematicalExpression(_Base, frozen=True):
    """A block with a mathematical expression in LaTeX format, corresponding to the custom HTML tag <tg-math-block>.
    
    https://core.telegram.org/bots/api#richblockmathematicalexpression
    """
    type: Literal["mathematical_expression"] = Field(default='mathematical_expression')
    """Type of the block, always "mathematical_expression" """
    expression: str
    """The mathematical expression in LaTeX format"""

class RichBlockAnchor(_Base, frozen=True):
    """A block with an anchor, corresponding to the HTML tag <a> with the attribute name.
    
    https://core.telegram.org/bots/api#richblockanchor
    """
    type: Literal["anchor"] = Field(default='anchor')
    """Type of the block, always "anchor" """
    name: str
    """The name of the anchor"""

class RichBlockList(_Base, frozen=True):
    """A list of blocks, corresponding to the HTML tag <ul> or <ol> with multiple nested tags <li>.
    
    https://core.telegram.org/bots/api#richblocklist
    """
    type: Literal["list"] = Field(default='list')
    """Type of the block, always "list" """
    items: List[RichBlockListItem]
    """Items of the list"""

class RichBlockBlockQuotation(_Base, frozen=True):
    """A block quotation, corresponding to the HTML tag <blockquote>.
    
    https://core.telegram.org/bots/api#richblockblockquotation
    """
    type: Literal["blockquote"] = Field(default='blockquote')
    """Type of the block, always "blockquote" """
    blocks: List[RichBlock]
    """Content of the block"""
    credit: Optional[RichText] = Field(default=None)
    """Optional. Credit of the block"""

class RichBlockExpandableBlockQuotation(_Base, frozen=True):
    """A block quotation, corresponding to the HTML tag <blockquote> with custom attribute "expandable".
    
    https://core.telegram.org/bots/api#richblockexpandableblockquotation
    """
    type: Literal["expandable_blockquote"] = Field(default='expandable_blockquote')
    """Type of the block, always "expandable_blockquote" """
    text: RichText
    """Content of the block"""
    credit: Optional[RichText] = Field(default=None)
    """Optional. Credit of the block"""

class RichBlockPullQuotation(_Base, frozen=True):
    """A quotation with centered text, loosely corresponding to the HTML tag <aside>.
    
    https://core.telegram.org/bots/api#richblockpullquotation
    """
    type: Literal["pullquote"] = Field(default='pullquote')
    """Type of the block, always "pullquote" """
    text: RichText
    """Text of the block"""
    credit: Optional[RichText] = Field(default=None)
    """Optional. Credit of the block"""

class RichBlockCollage(_Base, frozen=True):
    """A collage, corresponding to the custom HTML tag <tg-collage>.
    
    https://core.telegram.org/bots/api#richblockcollage
    """
    type: Literal["collage"] = Field(default='collage')
    """Type of the block, always "collage" """
    blocks: List[RichBlock]
    """Elements of the collage"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class RichBlockSlideshow(_Base, frozen=True):
    """A slideshow, corresponding to the custom HTML tag <tg-slideshow>.
    
    https://core.telegram.org/bots/api#richblockslideshow
    """
    type: Literal["slideshow"] = Field(default='slideshow')
    """Type of the block, always "slideshow" """
    blocks: List[RichBlock]
    """Elements of the slideshow"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class RichBlockTable(_Base, frozen=True):
    """A table, corresponding to the HTML tag <table>.
    
    https://core.telegram.org/bots/api#richblocktable
    """
    type: Literal["table"] = Field(default='table')
    """Type of the block, always "table" """
    cells: List[List[RichBlockTableCell]]
    """Cells of the table"""
    is_bordered: Optional[bool] = Field(default=None)
    """Optional. True, if the table has borders"""
    is_striped: Optional[bool] = Field(default=None)
    """Optional. True, if the table is striped"""
    is_compact: Optional[bool] = Field(default=None)
    """Optional. True, if table cells have smaller indents"""
    caption: Optional[RichText] = Field(default=None)
    """Optional. Caption of the table"""

class RichBlockDetails(_Base, frozen=True):
    """An expandable block for details disclosure, corresponding to the HTML tag <details>.
    
    https://core.telegram.org/bots/api#richblockdetails
    """
    type: Literal["details"] = Field(default='details')
    """Type of the block, always "details" """
    summary: RichText
    """Always shown summary of the block"""
    blocks: List[RichBlock]
    """Content of the block"""
    is_open: Optional[bool] = Field(default=None)
    """Optional. True, if the content of the block is visible by default"""

class RichBlockMap(_Base, frozen=True):
    """A block with a map, corresponding to the custom HTML tag <tg-map>.
    
    https://core.telegram.org/bots/api#richblockmap
    """
    type: Literal["map"] = Field(default='map')
    """Type of the block, always "map" """
    location: Location
    """Location of the center of the map"""
    zoom: int
    """Map zoom level"""
    width: int
    """Expected width of the map"""
    height: int
    """Expected height of the map"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class RichBlockButtons(_Base, frozen=True):
    """A block containing a list of buttons that are shown in one row, corresponding to the custom HTML tag <tg-button-row>.
    
    https://core.telegram.org/bots/api#richblockbuttons
    """
    type: Literal["buttons"] = Field(default='buttons')
    """Type of the block, always "buttons" """
    buttons: List[RichMessageButton]
    """The buttons"""
    align: Optional[str] = Field(default=None)
    """Optional. Horizontal alignment of the buttons. Currently, must be one of "left", "center", or "right"."""

class RichBlockAnimation(_Base, frozen=True):
    """A block with an animation, corresponding to the HTML tag <video>.
    
    https://core.telegram.org/bots/api#richblockanimation
    """
    type: Literal["animation"] = Field(default='animation')
    """Type of the block, always "animation" """
    animation: Animation
    """The animation"""
    has_spoiler: Optional[bool] = Field(default=None)
    """Optional. True, if the media preview is covered by a spoiler animation"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class RichBlockAudio(_Base, frozen=True):
    """A block with a music file, corresponding to the HTML tag <audio>.
    
    https://core.telegram.org/bots/api#richblockaudio
    """
    type: Literal["audio"] = Field(default='audio')
    """Type of the block, always "audio" """
    audio: Audio
    """The audio"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class RichBlockDocument(_Base, frozen=True):
    """A block with a general file, corresponding to the custom HTML tag <tg-document>.
    
    https://core.telegram.org/bots/api#richblockdocument
    """
    type: Literal["document"] = Field(default='document')
    """Type of the block, always "document" """
    document: Document
    """The document"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class RichBlockPhoto(_Base, frozen=True):
    """A block with a photo, corresponding to the HTML tag <img>.
    
    https://core.telegram.org/bots/api#richblockphoto
    """
    type: Literal["photo"] = Field(default='photo')
    """Type of the block, always "photo" """
    photo: List[PhotoSize]
    """Available sizes of the photo"""
    has_spoiler: Optional[bool] = Field(default=None)
    """Optional. True, if the media preview is covered by a spoiler animation"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class RichBlockVideo(_Base, frozen=True):
    """A block with a video, corresponding to the HTML tag <video>.
    
    https://core.telegram.org/bots/api#richblockvideo
    """
    type: Literal["video"] = Field(default='video')
    """Type of the block, always "video" """
    video: Video
    """The video"""
    has_spoiler: Optional[bool] = Field(default=None)
    """Optional. True, if the media preview is covered by a spoiler animation"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class RichBlockVoiceNote(_Base, frozen=True):
    """A block with a voice note, corresponding to the HTML tag <audio>.
    
    https://core.telegram.org/bots/api#richblockvoicenote
    """
    type: Literal["voice_note"] = Field(default='voice_note')
    """Type of the block, always "voice_note" """
    voice_note: Voice
    """The voice note"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class RichBlockThinking(_Base, frozen=True):
    """A block with a "Thinking..." placeholder, corresponding to the custom HTML tag <tg-thinking>. The block may be used only in sendRichMessageDraft, therefore it can't be received in messages. See https://t.me/addemoji/AIActions for examples of custom emoji that are recommended for usage in the block.
    
    https://core.telegram.org/bots/api#richblockthinking
    """
    type: Literal["thinking"] = Field(default='thinking')
    """Type of the block, always "thinking" """
    text: RichText
    """Text of the block. See https://t.me/addemoji/AIActions for examples of custom emoji that are recommended for usage in the block."""

class InputRichBlockListItem(_Base, frozen=True):
    """An item of a list to be sent.
    
    https://core.telegram.org/bots/api#inputrichblocklistitem
    """
    blocks: List[InputRichBlock]
    """The content of the item"""
    has_checkbox: Optional[bool] = Field(default=None)
    """Optional. Pass True if the item has a checkbox"""
    is_checked: Optional[bool] = Field(default=None)
    """Optional. Pass True if the item has a checked checkbox"""
    value: Optional[int] = Field(default=None)
    """Optional. For ordered lists, the numeric value of the item label"""
    type: Optional[str] = Field(default=None)
    """Optional. For ordered lists, the type of the item label; must be one of "a" for lowercase letters, "A" for uppercase letters, "i" for lowercase Roman numerals, "I" for uppercase Roman numerals, or "1" for decimal numbers"""

class InputRichBlockParagraph(_Base, frozen=True):
    """A text paragraph, corresponding to the HTML tag <p>.
    
    https://core.telegram.org/bots/api#inputrichblockparagraph
    """
    type: Literal["paragraph"] = Field(default='paragraph')
    """Type of the block, always "paragraph" """
    text: RichText
    """Text of the block"""

class InputRichBlockSectionHeading(_Base, frozen=True):
    """A section heading, corresponding to the HTML tags <h1>, <h2>, <h3>, <h4>, <h5>, or <h6>.
    
    https://core.telegram.org/bots/api#inputrichblocksectionheading
    """
    type: Literal["heading"] = Field(default='heading')
    """Type of the block, always "heading" """
    text: RichText
    """Text of the block"""
    size: int
    """Relative size of the text font; 1-6, 1 is the largest, 6 is the smallest"""

class InputRichBlockPreformatted(_Base, frozen=True):
    """A preformatted text block, corresponding to the nested HTML tags <pre> and <code>.
    
    https://core.telegram.org/bots/api#inputrichblockpreformatted
    """
    type: Literal["pre"] = Field(default='pre')
    """Type of the block, always "pre" """
    text: RichText
    """Text of the block"""
    language: Optional[str] = Field(default=None)
    """Optional. The programming language of the text"""

class InputRichBlockFooter(_Base, frozen=True):
    """A footer, corresponding to the HTML tag <footer>.
    
    https://core.telegram.org/bots/api#inputrichblockfooter
    """
    type: Literal["footer"] = Field(default='footer')
    """Type of the block, always "footer" """
    text: RichText
    """Text of the block"""

class InputRichBlockDivider(_Base, frozen=True):
    """A divider, corresponding to the HTML tag <hr/>.
    
    https://core.telegram.org/bots/api#inputrichblockdivider
    """
    type: Literal["divider"] = Field(default='divider')
    """Type of the block, always "divider" """

class InputRichBlockMathematicalExpression(_Base, frozen=True):
    """A block with a mathematical expression in LaTeX format, corresponding to the custom HTML tag <tg-math-block>.
    
    https://core.telegram.org/bots/api#inputrichblockmathematicalexpression
    """
    type: Literal["mathematical_expression"] = Field(default='mathematical_expression')
    """Type of the block, always "mathematical_expression" """
    expression: str
    """The mathematical expression in LaTeX format"""

class InputRichBlockAnchor(_Base, frozen=True):
    """A block with an anchor, corresponding to the HTML tag <a> with the attribute name.
    
    https://core.telegram.org/bots/api#inputrichblockanchor
    """
    type: Literal["anchor"] = Field(default='anchor')
    """Type of the block, always "anchor" """
    name: str
    """The name of the anchor"""

class InputRichBlockList(_Base, frozen=True):
    """A list of blocks, corresponding to the HTML tag <ul> or <ol> with multiple nested tags <li>.
    
    https://core.telegram.org/bots/api#inputrichblocklist
    """
    type: Literal["list"] = Field(default='list')
    """Type of the block, always "list" """
    items: List[InputRichBlockListItem]
    """Items of the list"""

class InputRichBlockBlockQuotation(_Base, frozen=True):
    """A block quotation, corresponding to the HTML tag <blockquote>.
    
    https://core.telegram.org/bots/api#inputrichblockblockquotation
    """
    type: Literal["blockquote"] = Field(default='blockquote')
    """Type of the block, always "blockquote" """
    blocks: List[InputRichBlock]
    """Content of the block"""
    credit: Optional[RichText] = Field(default=None)
    """Optional. Credit of the block"""

class InputRichBlockExpandableBlockQuotation(_Base, frozen=True):
    """A block quotation, corresponding to the HTML tag <blockquote> with custom attribute "expandable".
    
    https://core.telegram.org/bots/api#inputrichblockexpandableblockquotation
    """
    type: Literal["expandable_blockquote"] = Field(default='expandable_blockquote')
    """Type of the block, always "expandable_blockquote" """
    text: RichText
    """Content of the block"""
    credit: Optional[RichText] = Field(default=None)
    """Optional. Credit of the block"""

class InputRichBlockPullQuotation(_Base, frozen=True):
    """A quotation with centered text, loosely corresponding to the HTML tag <aside>.
    
    https://core.telegram.org/bots/api#inputrichblockpullquotation
    """
    type: Literal["pullquote"] = Field(default='pullquote')
    """Type of the block, always "pullquote" """
    text: RichText
    """Text of the block"""
    credit: Optional[RichText] = Field(default=None)
    """Optional. Credit of the block"""

class InputRichBlockCollage(_Base, frozen=True):
    """A collage, corresponding to the custom HTML tag <tg-collage>.
    
    https://core.telegram.org/bots/api#inputrichblockcollage
    """
    type: Literal["collage"] = Field(default='collage')
    """Type of the block, always "collage" """
    blocks: List[InputRichBlock]
    """Elements of the collage"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class InputRichBlockSlideshow(_Base, frozen=True):
    """A slideshow, corresponding to the custom HTML tag <tg-slideshow>.
    
    https://core.telegram.org/bots/api#inputrichblockslideshow
    """
    type: Literal["slideshow"] = Field(default='slideshow')
    """Type of the block, always "slideshow" """
    blocks: List[InputRichBlock]
    """Elements of the slideshow"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class InputRichBlockTable(_Base, frozen=True):
    """A table, corresponding to the HTML tag <table>.
    
    https://core.telegram.org/bots/api#inputrichblocktable
    """
    type: Literal["table"] = Field(default='table')
    """Type of the block, always "table" """
    cells: List[List[RichBlockTableCell]]
    """Cells of the table"""
    is_bordered: Optional[bool] = Field(default=None)
    """Optional. Pass True if the table has borders"""
    is_striped: Optional[bool] = Field(default=None)
    """Optional. Pass True if the table is striped"""
    is_compact: Optional[bool] = Field(default=None)
    """Optional. Pass True if table cells must have smaller indents"""
    caption: Optional[RichText] = Field(default=None)
    """Optional. Caption of the table"""

class InputRichBlockDetails(_Base, frozen=True):
    """An expandable block for details disclosure, corresponding to the HTML tag <details>.
    
    https://core.telegram.org/bots/api#inputrichblockdetails
    """
    type: Literal["details"] = Field(default='details')
    """Type of the block, always "details" """
    summary: RichText
    """Always shown summary of the block"""
    blocks: List[InputRichBlock]
    """Content of the block"""
    is_open: Optional[bool] = Field(default=None)
    """Optional. Pass True if the content of the block is visible by default"""

class InputRichBlockMap(_Base, frozen=True):
    """A block with a map, corresponding to the custom HTML tag <tg-map>. The map's width and height must not exceed 10000 in total. The width and height ratio must be at most 20.
    
    https://core.telegram.org/bots/api#inputrichblockmap
    """
    type: Literal["map"] = Field(default='map')
    """Type of the block, always "map" """
    location: Location
    """Location of the center of the map"""
    zoom: Optional[int] = Field(default=None)
    """Optional. Map zoom level; 0-24"""
    width: Optional[int] = Field(default=None)
    """Optional. Map width; 0-10000"""
    height: Optional[int] = Field(default=None)
    """Optional. Map height; 0-10000"""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class InputRichBlockButtons(_Base, frozen=True):
    """A block containing a list of buttons that are shown in one row, corresponding to the custom HTML tag <tg-button-row>.
    
    https://core.telegram.org/bots/api#inputrichblockbuttons
    """
    type: Literal["buttons"] = Field(default='buttons')
    """Type of the block, always "buttons" """
    buttons: List[RichMessageButton]
    """List of 1-8 buttons to send"""
    align: Optional[str] = Field(default=None)
    """Optional. Horizontal alignment of the buttons. Currently, must be one of "left", "center", or "right"."""

class InputRichBlockAnimation(_Base, frozen=True):
    """A block with an animation, corresponding to the HTML tag <video>.
    
    https://core.telegram.org/bots/api#inputrichblockanimation
    """
    type: Literal["animation"] = Field(default='animation')
    """Type of the block, always "animation" """
    animation: InputMediaAnimation
    """The animation. Caption is ignored."""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class InputRichBlockAudio(_Base, frozen=True):
    """A block with a music file, corresponding to the HTML tag <audio>.
    
    https://core.telegram.org/bots/api#inputrichblockaudio
    """
    type: Literal["audio"] = Field(default='audio')
    """Type of the block, always "audio" """
    audio: InputMediaAudio
    """The audio. Caption is ignored."""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class InputRichBlockDocument(_Base, frozen=True):
    """A block with a general file, corresponding to the custom HTML tag <tg-document>.
    
    https://core.telegram.org/bots/api#inputrichblockdocument
    """
    type: Literal["document"] = Field(default='document')
    """Type of the block, always "document" """
    document: InputMediaDocument
    """The document. Caption is ignored."""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class InputRichBlockPhoto(_Base, frozen=True):
    """A block with a photo, corresponding to the HTML tag <img>.
    
    https://core.telegram.org/bots/api#inputrichblockphoto
    """
    type: Literal["photo"] = Field(default='photo')
    """Type of the block, always "photo" """
    photo: InputMediaPhoto
    """The photo. Caption is ignored."""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class InputRichBlockVideo(_Base, frozen=True):
    """A block with a video, corresponding to the HTML tag <video>.
    
    https://core.telegram.org/bots/api#inputrichblockvideo
    """
    type: Literal["video"] = Field(default='video')
    """Type of the block, always "video" """
    video: InputMediaVideo
    """The video. Caption is ignored."""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class InputRichBlockVoiceNote(_Base, frozen=True):
    """A block with a voice note, corresponding to the HTML tag <audio>.
    
    https://core.telegram.org/bots/api#inputrichblockvoicenote
    """
    type: Literal["voice_note"] = Field(default='voice_note')
    """Type of the block, always "voice_note" """
    voice_note: InputMediaVoiceNote
    """The voice note. Caption is ignored."""
    caption: Optional[RichBlockCaption] = Field(default=None)
    """Optional. Caption of the block"""

class InputRichBlockThinking(_Base, frozen=True):
    """A block with a "Thinking..." placeholder, corresponding to the custom HTML tag <tg-thinking>. The block may be used only in sendRichMessageDraft, therefore it can't be received in messages. See https://t.me/addemoji/AIActions for examples of custom emoji that are recommended for usage in the block.
    
    https://core.telegram.org/bots/api#inputrichblockthinking
    """
    type: Literal["thinking"] = Field(default='thinking')
    """Type of the block, always "thinking" """
    text: RichText
    """Text of the block. See https://t.me/addemoji/AIActions for examples of custom emoji that are recommended for usage in the block."""

class InlineQuery(_Base, frozen=True):
    """This object represents an incoming inline query. When the user sends an empty query, your bot could return some default or trending results.
    
    https://core.telegram.org/bots/api#inlinequery
    """
    id: str
    """Unique identifier for this query"""
    user: User = Field(alias='from')
    """Sender"""
    query: str
    """Text of the query (up to 256 characters)"""
    offset: str
    """Offset of the results to be returned, can be controlled by the bot"""
    chat_type: Optional[str] = Field(default=None)
    """Optional. Type of the chat from which the inline query was sent. Can be either "sender" for a private chat with the inline query sender, "private", "group", "supergroup", or "channel". The chat type should be always known for requests sent from official clients and most third-party clients, unless the request was sent from a secret chat."""
    location: Optional[Location] = Field(default=None)
    """Optional. Sender location, only for bots that request user location"""

    async def answer(
        self,
        results: List[InlineQueryResult],
        *,
        cache_time: Optional[int] = None,
        is_personal: Optional[bool] = None,
        next_offset: Optional[str] = None,
        button: Optional[InlineQueryResultsButton] = None,
    ) -> bool:
        """Как bot.answer_inline_query(), но id запроса берётся из объекта.
        
        Use this method to send answers to an inline query. On success, True is returned.
        
        No more than 50 results per query are allowed.
        
        https://core.telegram.org/bots/api#answerinlinequery
        """
        return await self._require_bot().answer_inline_query(
            inline_query_id=self.id,
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            button=button,
        )

class InlineQueryResultsButton(_Base, frozen=True):
    """This object represents a button to be shown above inline query results. You must use exactly one of the optional fields.
    
    https://core.telegram.org/bots/api#inlinequeryresultsbutton
    """
    text: str
    """Label text on the button"""
    web_app: Optional[WebAppInfo] = Field(default=None)
    """Optional. Description of the Web App that will be launched when the user presses the button. The Web App will be able to switch back to the inline mode using the method switchInlineQuery inside the Web App."""
    start_parameter: Optional[str] = Field(default=None)
    """Optional. Deep-linking parameter for the /start message sent to the bot when a user presses the button. 1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed. Example: An inline bot that sends YouTube videos can ask the user to connect the bot to their YouTube account to adapt search results accordingly. To do this, it displays a 'Connect your YouTube account' button above the results, or even before showing any. The user presses the button, switches to a private chat with the bot and, in doing so, passes a start parameter that instructs the bot to return an OAuth link. Once done, the bot can offer a switch_inline button so that the user can easily return to the chat where they wanted to use the bot's inline capabilities."""

class InlineQueryResultArticle(_Base, frozen=True):
    """Represents a link to an article or web page.
    
    https://core.telegram.org/bots/api#inlinequeryresultarticle
    """
    type: Literal["article"] = Field(default='article')
    """Type of the result, must be article"""
    id: str
    """Unique identifier for this result, 1-64 Bytes"""
    title: str
    """Title of the result"""
    input_message_content: InputMessageContent
    """Content of the message to be sent"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    url: Optional[str] = Field(default=None)
    """Optional. URL of the result"""
    description: Optional[str] = Field(default=None)
    """Optional. Short description of the result"""
    thumbnail_url: Optional[str] = Field(default=None)
    """Optional. Url of the thumbnail for the result"""
    thumbnail_width: Optional[int] = Field(default=None)
    """Optional. Thumbnail width"""
    thumbnail_height: Optional[int] = Field(default=None)
    """Optional. Thumbnail height"""

class InlineQueryResultPhoto(_Base, frozen=True):
    """Represents a link to a photo. By default, this photo will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.
    
    https://core.telegram.org/bots/api#inlinequeryresultphoto
    """
    type: Literal["photo"] = Field(default='photo')
    """Type of the result, must be photo"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    photo_url: str
    """A valid URL of the photo. Photo must be in JPEG format. Photo size must not exceed 5MB."""
    thumbnail_url: str
    """URL of the thumbnail for the photo"""
    photo_width: Optional[int] = Field(default=None)
    """Optional. Width of the photo"""
    photo_height: Optional[int] = Field(default=None)
    """Optional. Height of the photo"""
    title: Optional[str] = Field(default=None)
    """Optional. Title for the result"""
    description: Optional[str] = Field(default=None)
    """Optional. Short description of the result"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the photo caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the photo"""

class InlineQueryResultGif(_Base, frozen=True):
    """Represents a link to an animated GIF file. By default, this animated GIF file will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.
    
    https://core.telegram.org/bots/api#inlinequeryresultgif
    """
    type: Literal["gif"] = Field(default='gif')
    """Type of the result, must be gif"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    gif_url: str
    """A valid URL for the GIF file"""
    gif_width: Optional[int] = Field(default=None)
    """Optional. Width of the GIF"""
    gif_height: Optional[int] = Field(default=None)
    """Optional. Height of the GIF"""
    gif_duration: Optional[int] = Field(default=None)
    """Optional. Duration of the GIF in seconds"""
    thumbnail_url: str
    """URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the result"""
    thumbnail_mime_type: Optional[str] = Field(default=None)
    """Optional. MIME type of the thumbnail, must be one of "image/jpeg", "image/gif", or "video/mp4". Defaults to "image/jpeg"."""
    title: Optional[str] = Field(default=None)
    """Optional. Title for the result"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the GIF file to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the GIF animation"""

class InlineQueryResultMpeg4Gif(_Base, frozen=True):
    """Represents a link to a video animation (H.264/MPEG-4 AVC video without sound). By default, this animated MPEG-4 file will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.
    
    https://core.telegram.org/bots/api#inlinequeryresultmpeg4gif
    """
    type: Literal["mpeg4_gif"] = Field(default='mpeg4_gif')
    """Type of the result, must be mpeg4_gif"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    mpeg4_url: str
    """A valid URL for the MPEG4 file"""
    mpeg4_width: Optional[int] = Field(default=None)
    """Optional. Video width"""
    mpeg4_height: Optional[int] = Field(default=None)
    """Optional. Video height"""
    mpeg4_duration: Optional[int] = Field(default=None)
    """Optional. Video duration in seconds"""
    thumbnail_url: str
    """URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the result"""
    thumbnail_mime_type: Optional[str] = Field(default=None)
    """Optional. MIME type of the thumbnail, must be one of "image/jpeg", "image/gif", or "video/mp4". Defaults to "image/jpeg"."""
    title: Optional[str] = Field(default=None)
    """Optional. Title for the result"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the MPEG-4 file to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the video animation"""

class InlineQueryResultVideo(_Base, frozen=True):
    """Represents a link to a page containing an embedded video player or a video file. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the video.
    
    https://core.telegram.org/bots/api#inlinequeryresultvideo
    """
    type: Literal["video"] = Field(default='video')
    """Type of the result, must be video"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    video_url: str
    """A valid URL for the embedded video player or video file"""
    mime_type: str
    """MIME type of the content of the video URL, "text/html" or "video/mp4" """
    thumbnail_url: str
    """URL of the thumbnail (JPEG only) for the video"""
    title: str
    """Title for the result"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the video to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the video caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    video_width: Optional[int] = Field(default=None)
    """Optional. Video width"""
    video_height: Optional[int] = Field(default=None)
    """Optional. Video height"""
    video_duration: Optional[int] = Field(default=None)
    """Optional. Video duration in seconds"""
    description: Optional[str] = Field(default=None)
    """Optional. Short description of the result"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the video. This field is required if InlineQueryResultVideo is used to send an HTML-page as a result (e.g., a YouTube video)."""

class InlineQueryResultAudio(_Base, frozen=True):
    """Represents a link to an MP3 audio file. By default, this audio file will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.
    
    https://core.telegram.org/bots/api#inlinequeryresultaudio
    """
    type: Literal["audio"] = Field(default='audio')
    """Type of the result, must be audio"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    audio_url: str
    """A valid URL for the audio file"""
    title: str
    """Title"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the audio caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    performer: Optional[str] = Field(default=None)
    """Optional. Performer"""
    audio_duration: Optional[int] = Field(default=None)
    """Optional. Audio duration in seconds"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the audio"""

class InlineQueryResultVoice(_Base, frozen=True):
    """Represents a link to a voice recording in an .OGG container encoded with OPUS. By default, this voice recording will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the the voice message.
    
    https://core.telegram.org/bots/api#inlinequeryresultvoice
    """
    type: Literal["voice"] = Field(default='voice')
    """Type of the result, must be voice"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    voice_url: str
    """A valid URL for the voice recording"""
    title: str
    """Recording title"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the voice message caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    voice_duration: Optional[int] = Field(default=None)
    """Optional. Recording duration in seconds"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the voice recording"""

class InlineQueryResultDocument(_Base, frozen=True):
    """Represents a link to a file. By default, this file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the file. Currently, only .PDF and .ZIP files can be sent using this method.
    
    https://core.telegram.org/bots/api#inlinequeryresultdocument
    """
    type: Literal["document"] = Field(default='document')
    """Type of the result, must be document"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    title: str
    """Title for the result"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the document to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the document caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    document_url: str
    """A valid URL for the file"""
    mime_type: str
    """MIME type of the content of the file, either "application/pdf" or "application/zip" """
    description: Optional[str] = Field(default=None)
    """Optional. Short description of the result"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the file"""
    thumbnail_url: Optional[str] = Field(default=None)
    """Optional. URL of the thumbnail (JPEG only) for the file"""
    thumbnail_width: Optional[int] = Field(default=None)
    """Optional. Thumbnail width"""
    thumbnail_height: Optional[int] = Field(default=None)
    """Optional. Thumbnail height"""

class InlineQueryResultLocation(_Base, frozen=True):
    """Represents a location on a map. By default, the location will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the location.
    
    https://core.telegram.org/bots/api#inlinequeryresultlocation
    """
    type: Literal["location"] = Field(default='location')
    """Type of the result, must be location"""
    id: str
    """Unique identifier for this result, 1-64 Bytes"""
    latitude: float
    """Location latitude in degrees"""
    longitude: float
    """Location longitude in degrees"""
    title: str
    """Location title"""
    horizontal_accuracy: Optional[float] = Field(default=None)
    """Optional. The radius of uncertainty for the location, measured in meters; 0-1500"""
    live_period: Optional[int] = Field(default=None)
    """Optional. Period in seconds during which the location can be updated, must be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely"""
    heading: Optional[int] = Field(default=None)
    """Optional. For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified."""
    proximity_alert_radius: Optional[int] = Field(default=None)
    """Optional. For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified."""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the location"""
    thumbnail_url: Optional[str] = Field(default=None)
    """Optional. Url of the thumbnail for the result"""
    thumbnail_width: Optional[int] = Field(default=None)
    """Optional. Thumbnail width"""
    thumbnail_height: Optional[int] = Field(default=None)
    """Optional. Thumbnail height"""

class InlineQueryResultVenue(_Base, frozen=True):
    """Represents a venue. By default, the venue will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the venue.
    
    https://core.telegram.org/bots/api#inlinequeryresultvenue
    """
    type: Literal["venue"] = Field(default='venue')
    """Type of the result, must be venue"""
    id: str
    """Unique identifier for this result, 1-64 Bytes"""
    latitude: float
    """Latitude of the venue location in degrees"""
    longitude: float
    """Longitude of the venue location in degrees"""
    title: str
    """Title of the venue"""
    address: str
    """Address of the venue"""
    foursquare_id: Optional[str] = Field(default=None)
    """Optional. Foursquare identifier of the venue if known"""
    foursquare_type: Optional[str] = Field(default=None)
    """Optional. Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)"""
    google_place_id: Optional[str] = Field(default=None)
    """Optional. Google Places identifier of the venue"""
    google_place_type: Optional[str] = Field(default=None)
    """Optional. Google Places type of the venue. (See supported types.)"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the venue"""
    thumbnail_url: Optional[str] = Field(default=None)
    """Optional. Url of the thumbnail for the result"""
    thumbnail_width: Optional[int] = Field(default=None)
    """Optional. Thumbnail width"""
    thumbnail_height: Optional[int] = Field(default=None)
    """Optional. Thumbnail height"""

class InlineQueryResultContact(_Base, frozen=True):
    """Represents a contact with a phone number. By default, this contact will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the contact.
    
    https://core.telegram.org/bots/api#inlinequeryresultcontact
    """
    type: Literal["contact"] = Field(default='contact')
    """Type of the result, must be contact"""
    id: str
    """Unique identifier for this result, 1-64 Bytes"""
    phone_number: str
    """Contact's phone number"""
    first_name: str
    """Contact's first name"""
    last_name: Optional[str] = Field(default=None)
    """Optional. Contact's last name"""
    vcard: Optional[str] = Field(default=None)
    """Optional. Additional data about the contact in the form of a vCard, 0-2048 bytes"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the contact"""
    thumbnail_url: Optional[str] = Field(default=None)
    """Optional. Url of the thumbnail for the result"""
    thumbnail_width: Optional[int] = Field(default=None)
    """Optional. Thumbnail width"""
    thumbnail_height: Optional[int] = Field(default=None)
    """Optional. Thumbnail height"""

class InlineQueryResultGame(_Base, frozen=True):
    """Represents a Game.
    
    https://core.telegram.org/bots/api#inlinequeryresultgame
    """
    type: Literal["game"] = Field(default='game')
    """Type of the result, must be game"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    game_short_name: str
    """Short name of the game"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""

class InlineQueryResultCachedPhoto(_Base, frozen=True):
    """Represents a link to a photo stored on the Telegram servers. By default, this photo will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.
    
    https://core.telegram.org/bots/api#inlinequeryresultcachedphoto
    """
    type: Literal["photo"] = Field(default='photo')
    """Type of the result, must be photo"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    photo_file_id: str
    """A valid file identifier of the photo"""
    title: Optional[str] = Field(default=None)
    """Optional. Title for the result"""
    description: Optional[str] = Field(default=None)
    """Optional. Short description of the result"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the photo caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the photo"""

class InlineQueryResultCachedGif(_Base, frozen=True):
    """Represents a link to an animated GIF file stored on the Telegram servers. By default, this animated GIF file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with specified content instead of the animation.
    
    https://core.telegram.org/bots/api#inlinequeryresultcachedgif
    """
    type: Literal["gif"] = Field(default='gif')
    """Type of the result, must be gif"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    gif_file_id: str
    """A valid file identifier for the GIF file"""
    title: Optional[str] = Field(default=None)
    """Optional. Title for the result"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the GIF file to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the GIF animation"""

class InlineQueryResultCachedMpeg4Gif(_Base, frozen=True):
    """Represents a link to a video animation (H.264/MPEG-4 AVC video without sound) stored on the Telegram servers. By default, this animated MPEG-4 file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.
    
    https://core.telegram.org/bots/api#inlinequeryresultcachedmpeg4gif
    """
    type: Literal["mpeg4_gif"] = Field(default='mpeg4_gif')
    """Type of the result, must be mpeg4_gif"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    mpeg4_file_id: str
    """A valid file identifier for the MPEG4 file"""
    title: Optional[str] = Field(default=None)
    """Optional. Title for the result"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the MPEG-4 file to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the video animation"""

class InlineQueryResultCachedSticker(_Base, frozen=True):
    """Represents a link to a sticker stored on the Telegram servers. By default, this sticker will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the sticker.
    
    https://core.telegram.org/bots/api#inlinequeryresultcachedsticker
    """
    type: Literal["sticker"] = Field(default='sticker')
    """Type of the result, must be sticker"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    sticker_file_id: str
    """A valid file identifier of the sticker"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the sticker"""

class InlineQueryResultCachedDocument(_Base, frozen=True):
    """Represents a link to a file stored on the Telegram servers. By default, this file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the file.
    
    https://core.telegram.org/bots/api#inlinequeryresultcacheddocument
    """
    type: Literal["document"] = Field(default='document')
    """Type of the result, must be document"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    title: str
    """Title for the result"""
    document_file_id: str
    """A valid file identifier for the file"""
    description: Optional[str] = Field(default=None)
    """Optional. Short description of the result"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the document to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the document caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the file"""

class InlineQueryResultCachedVideo(_Base, frozen=True):
    """Represents a link to a video file stored on the Telegram servers. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the video.
    
    https://core.telegram.org/bots/api#inlinequeryresultcachedvideo
    """
    type: Literal["video"] = Field(default='video')
    """Type of the result, must be video"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    video_file_id: str
    """A valid file identifier for the video file"""
    title: str
    """Title for the result"""
    description: Optional[str] = Field(default=None)
    """Optional. Short description of the result"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption of the video to be sent, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the video caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    show_caption_above_media: Optional[bool] = Field(default=None)
    """Optional. Pass True if the caption must be shown above the message media"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the video"""

class InlineQueryResultCachedVoice(_Base, frozen=True):
    """Represents a link to a voice message stored on the Telegram servers. By default, this voice message will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the voice message.
    
    https://core.telegram.org/bots/api#inlinequeryresultcachedvoice
    """
    type: Literal["voice"] = Field(default='voice')
    """Type of the result, must be voice"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    voice_file_id: str
    """A valid file identifier for the voice message"""
    title: str
    """Voice message title"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the voice message caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the voice message"""

class InlineQueryResultCachedAudio(_Base, frozen=True):
    """Represents a link to an MP3 audio file stored on the Telegram servers. By default, this audio file will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.
    
    https://core.telegram.org/bots/api#inlinequeryresultcachedaudio
    """
    type: Literal["audio"] = Field(default='audio')
    """Type of the result, must be audio"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    audio_file_id: str
    """A valid file identifier for the audio file"""
    caption: Optional[str] = Field(default=None)
    """Optional. Caption, 0-1024 characters after entities parsing"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the audio caption. See formatting options for more details."""
    caption_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode"""
    reply_markup: Optional[InlineKeyboardMarkup] = Field(default=None)
    """Optional. Inline keyboard attached to the message"""
    input_message_content: Optional[InputMessageContent] = Field(default=None)
    """Optional. Content of the message to be sent instead of the audio"""

class InputTextMessageContent(_Base, frozen=True):
    """Represents the content of a text message to be sent as the result of an inline query.
    
    https://core.telegram.org/bots/api#inputtextmessagecontent
    """
    message_text: str
    """Text of the message to be sent, 1-4096 characters"""
    parse_mode: Optional[str] = Field(default=None)
    """Optional. Mode for parsing entities in the message text. See formatting options for more details."""
    entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. List of special entities that appear in message text, which can be specified instead of parse_mode"""
    link_preview_options: Optional[LinkPreviewOptions] = Field(default=None)
    """Optional. Link preview generation options for the message"""

class InputRichMessageContent(_Base, frozen=True):
    """Represents the content of a rich message to be sent as the result of an inline query.
    
    https://core.telegram.org/bots/api#inputrichmessagecontent
    """
    rich_message: InputRichMessage
    """The message to be sent. Only previously uploaded files may be used in the message."""

class InputLocationMessageContent(_Base, frozen=True):
    """Represents the content of a location message to be sent as the result of an inline query.
    
    https://core.telegram.org/bots/api#inputlocationmessagecontent
    """
    latitude: float
    """Latitude of the location in degrees"""
    longitude: float
    """Longitude of the location in degrees"""
    horizontal_accuracy: Optional[float] = Field(default=None)
    """Optional. The radius of uncertainty for the location, measured in meters; 0-1500"""
    live_period: Optional[int] = Field(default=None)
    """Optional. Period in seconds during which the location can be updated, must be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely"""
    heading: Optional[int] = Field(default=None)
    """Optional. For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified."""
    proximity_alert_radius: Optional[int] = Field(default=None)
    """Optional. For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified."""

class InputVenueMessageContent(_Base, frozen=True):
    """Represents the content of a venue message to be sent as the result of an inline query.
    
    https://core.telegram.org/bots/api#inputvenuemessagecontent
    """
    latitude: float
    """Latitude of the venue in degrees"""
    longitude: float
    """Longitude of the venue in degrees"""
    title: str
    """Name of the venue"""
    address: str
    """Address of the venue"""
    foursquare_id: Optional[str] = Field(default=None)
    """Optional. Foursquare identifier of the venue, if known"""
    foursquare_type: Optional[str] = Field(default=None)
    """Optional. Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)"""
    google_place_id: Optional[str] = Field(default=None)
    """Optional. Google Places identifier of the venue"""
    google_place_type: Optional[str] = Field(default=None)
    """Optional. Google Places type of the venue. (See supported types.)"""

class InputContactMessageContent(_Base, frozen=True):
    """Represents the content of a contact message to be sent as the result of an inline query.
    
    https://core.telegram.org/bots/api#inputcontactmessagecontent
    """
    phone_number: str
    """Contact's phone number"""
    first_name: str
    """Contact's first name"""
    last_name: Optional[str] = Field(default=None)
    """Optional. Contact's last name"""
    vcard: Optional[str] = Field(default=None)
    """Optional. Additional data about the contact in the form of a vCard, 0-2048 bytes"""

class InputInvoiceMessageContent(_Base, frozen=True):
    """Represents the content of an invoice message to be sent as the result of an inline query.
    
    https://core.telegram.org/bots/api#inputinvoicemessagecontent
    """
    title: str
    """Product name, 1-32 characters"""
    description: str
    """Product description, 1-255 characters"""
    payload: str
    """Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes."""
    provider_token: Optional[str] = Field(default=None)
    """Optional. Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars."""
    currency: str
    """Three-letter ISO 4217 currency code, see more on currencies. Pass "XTR" for payments in Telegram Stars."""
    prices: List[LabeledPrice]
    """Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain exactly one item for payments in Telegram Stars."""
    max_tip_amount: Optional[int] = Field(default=None)
    """Optional. The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars."""
    suggested_tip_amounts: Optional[List[int]] = Field(default=None)
    """Optional. A JSON-serialized Array of suggested amounts of tip in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount."""
    provider_data: Optional[str] = Field(default=None)
    """Optional. A JSON-serialized object for data about the invoice, which will be shared with the payment provider. A detailed description of the required fields should be provided by the payment provider."""
    photo_url: Optional[str] = Field(default=None)
    """Optional. URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service."""
    photo_size: Optional[int] = Field(default=None)
    """Optional. Photo size in bytes"""
    photo_width: Optional[int] = Field(default=None)
    """Optional. Photo width"""
    photo_height: Optional[int] = Field(default=None)
    """Optional. Photo height"""
    need_name: Optional[bool] = Field(default=None)
    """Optional. Pass True if you require the user's full name to complete the order. Ignored for payments in Telegram Stars."""
    need_phone_number: Optional[bool] = Field(default=None)
    """Optional. Pass True if you require the user's phone number to complete the order. Ignored for payments in Telegram Stars."""
    need_email: Optional[bool] = Field(default=None)
    """Optional. Pass True if you require the user's email address to complete the order. Ignored for payments in Telegram Stars."""
    need_shipping_address: Optional[bool] = Field(default=None)
    """Optional. Pass True if you require the user's shipping address to complete the order. Ignored for payments in Telegram Stars."""
    send_phone_number_to_provider: Optional[bool] = Field(default=None)
    """Optional. Pass True if the user's phone number should be sent to the provider. Ignored for payments in Telegram Stars."""
    send_email_to_provider: Optional[bool] = Field(default=None)
    """Optional. Pass True if the user's email address should be sent to the provider. Ignored for payments in Telegram Stars."""
    is_flexible: Optional[bool] = Field(default=None)
    """Optional. Pass True if the final price depends on the shipping method. Ignored for payments in Telegram Stars."""

class ChosenInlineResult(_Base, frozen=True):
    """Represents a result of an inline query that was chosen by the user and sent to their chat partner.
    
    Note: It is necessary to enable inline feedback via @BotFather in order to receive these objects in updates.
    
    https://core.telegram.org/bots/api#choseninlineresult
    """
    result_id: str
    """The unique identifier for the result that was chosen"""
    user: User = Field(alias='from')
    """The user that chose the result"""
    location: Optional[Location] = Field(default=None)
    """Optional. Sender location, only for bots that require user location"""
    inline_message_id: Optional[str] = Field(default=None)
    """Optional. Identifier of the sent inline message. Available only if there is an inline keyboard attached to the message. Will be also received in callback queries and can be used to edit the message."""
    query: str
    """The query that was used to obtain the result"""

class LabeledPrice(_Base, frozen=True):
    """This object represents a portion of the price for goods or services.
    
    https://core.telegram.org/bots/api#labeledprice
    """
    label: str
    """Portion label"""
    amount: int
    """Price of the product in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies)."""

class Invoice(_Base, frozen=True):
    """This object contains basic information about an invoice.
    
    https://core.telegram.org/bots/api#invoice
    """
    title: str
    """Product name"""
    description: str
    """Product description"""
    start_parameter: str
    """Unique bot deep-linking parameter that can be used to generate this invoice"""
    currency: str
    """Three-letter ISO 4217 currency code, or "XTR" for payments in Telegram Stars"""
    total_amount: int
    """Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies)."""

class ShippingAddress(_Base, frozen=True):
    """This object represents a shipping address.
    
    https://core.telegram.org/bots/api#shippingaddress
    """
    country_code: str
    """Two-letter ISO 3166-1 alpha-2 country code"""
    state: str
    """State, if applicable"""
    city: str
    """City"""
    street_line1: str
    """First line for the address"""
    street_line2: str
    """Second line for the address"""
    post_code: str
    """Address post code"""

class OrderInfo(_Base, frozen=True):
    """This object represents information about an order.
    
    https://core.telegram.org/bots/api#orderinfo
    """
    name: Optional[str] = Field(default=None)
    """Optional. User name"""
    phone_number: Optional[str] = Field(default=None)
    """Optional. User's phone number"""
    email: Optional[str] = Field(default=None)
    """Optional. User email"""
    shipping_address: Optional[ShippingAddress] = Field(default=None)
    """Optional. User shipping address"""

class ShippingOption(_Base, frozen=True):
    """This object represents one shipping option.
    
    https://core.telegram.org/bots/api#shippingoption
    """
    id: str
    """Shipping option identifier"""
    title: str
    """Option title"""
    prices: List[LabeledPrice]
    """List of price portions"""

class SuccessfulPayment(_Base, frozen=True):
    """This object contains basic information about a successful payment. Note that if the buyer initiates a chargeback with the relevant payment provider following this transaction, the funds may be debited from your balance. This is outside of Telegram's control.
    
    https://core.telegram.org/bots/api#successfulpayment
    """
    currency: str
    """Three-letter ISO 4217 currency code, or "XTR" for payments in Telegram Stars"""
    total_amount: int
    """Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies)."""
    invoice_payload: str
    """Bot-specified invoice payload"""
    subscription_expiration_date: Optional[int] = Field(default=None)
    """Optional. Expiration date of the subscription, in Unix time; for recurring payments only"""
    is_recurring: Optional[bool] = Field(default=None)
    """Optional. True, if the payment is a recurring payment for a subscription"""
    is_first_recurring: Optional[bool] = Field(default=None)
    """Optional. True, if the payment is the first payment for a subscription"""
    shipping_option_id: Optional[str] = Field(default=None)
    """Optional. Identifier of the shipping option chosen by the user"""
    order_info: Optional[OrderInfo] = Field(default=None)
    """Optional. Order information provided by the user"""
    telegram_payment_charge_id: str
    """Telegram payment identifier"""
    provider_payment_charge_id: str
    """Provider payment identifier"""

class RefundedPayment(_Base, frozen=True):
    """This object contains basic information about a refunded payment.
    
    https://core.telegram.org/bots/api#refundedpayment
    """
    currency: str
    """Three-letter ISO 4217 currency code, or "XTR" for payments in Telegram Stars. Currently, always "XTR"."""
    total_amount: int
    """Total refunded price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45, total_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies)."""
    invoice_payload: str
    """Bot-specified invoice payload"""
    telegram_payment_charge_id: str
    """Telegram payment identifier"""
    provider_payment_charge_id: Optional[str] = Field(default=None)
    """Optional. Provider payment identifier"""

class ShippingQuery(_Base, frozen=True):
    """This object contains information about an incoming shipping query.
    
    https://core.telegram.org/bots/api#shippingquery
    """
    id: str
    """Unique query identifier"""
    user: User = Field(alias='from')
    """User who sent the query"""
    invoice_payload: str
    """Bot-specified invoice payload"""
    shipping_address: ShippingAddress
    """User specified shipping address"""

    async def answer(
        self,
        ok: bool,
        *,
        shipping_options: Optional[List[ShippingOption]] = None,
        error_message: Optional[str] = None,
    ) -> bool:
        """Как bot.answer_shipping_query(), но id запроса берётся из объекта.
        
        If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a shipping_query field to the bot. Use this method to reply to shipping queries. On success, True is returned.
        
        https://core.telegram.org/bots/api#answershippingquery
        """
        return await self._require_bot().answer_shipping_query(
            shipping_query_id=self.id,
            ok=ok,
            shipping_options=shipping_options,
            error_message=error_message,
        )

class PreCheckoutQuery(_Base, frozen=True):
    """This object contains information about an incoming pre-checkout query.
    
    https://core.telegram.org/bots/api#precheckoutquery
    """
    id: str
    """Unique query identifier"""
    user: User = Field(alias='from')
    """User who sent the query"""
    currency: str
    """Three-letter ISO 4217 currency code, or "XTR" for payments in Telegram Stars"""
    total_amount: int
    """Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies)."""
    invoice_payload: str
    """Bot-specified invoice payload"""
    shipping_option_id: Optional[str] = Field(default=None)
    """Optional. Identifier of the shipping option chosen by the user"""
    order_info: Optional[OrderInfo] = Field(default=None)
    """Optional. Order information provided by the user"""

    async def answer(
        self,
        ok: bool,
        *,
        error_message: Optional[str] = None,
    ) -> bool:
        """Как bot.answer_pre_checkout_query(), но id запроса берётся из объекта.
        
        Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an Update with the field pre_checkout_query. Use this method to respond to such pre-checkout queries. On success, True is returned. Note: The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent.
        
        https://core.telegram.org/bots/api#answerprecheckoutquery
        """
        return await self._require_bot().answer_pre_checkout_query(
            pre_checkout_query_id=self.id,
            ok=ok,
            error_message=error_message,
        )

class PaidMediaPurchased(_Base, frozen=True):
    """This object contains information about a paid media purchase.
    
    https://core.telegram.org/bots/api#paidmediapurchased
    """
    user: User = Field(alias='from')
    """User who purchased the media"""
    paid_media_payload: str
    """Bot-specified paid media payload"""

class RevenueWithdrawalStatePending(_Base, frozen=True):
    """The withdrawal is in progress.
    
    https://core.telegram.org/bots/api#revenuewithdrawalstatepending
    """
    type: Literal["pending"] = Field(default='pending')
    """Type of the state, always "pending" """

class RevenueWithdrawalStateSucceeded(_Base, frozen=True):
    """The withdrawal succeeded.
    
    https://core.telegram.org/bots/api#revenuewithdrawalstatesucceeded
    """
    type: Literal["succeeded"] = Field(default='succeeded')
    """Type of the state, always "succeeded" """
    date: int
    """Date the withdrawal was completed in Unix time"""
    url: str
    """An HTTPS URL that can be used to see transaction details"""

class RevenueWithdrawalStateFailed(_Base, frozen=True):
    """The withdrawal failed and the transaction was refunded.
    
    https://core.telegram.org/bots/api#revenuewithdrawalstatefailed
    """
    type: Literal["failed"] = Field(default='failed')
    """Type of the state, always "failed" """

class AffiliateInfo(_Base, frozen=True):
    """Contains information about the affiliate that received a commission via this transaction.
    
    https://core.telegram.org/bots/api#affiliateinfo
    """
    affiliate_user: Optional[User] = Field(default=None)
    """Optional. The bot or the user that received an affiliate commission if it was received by a bot or a user"""
    affiliate_chat: Optional[Chat] = Field(default=None)
    """Optional. The chat that received an affiliate commission if it was received by a chat"""
    commission_per_mille: int
    """The number of Telegram Stars received by the affiliate for each 1000 Telegram Stars received by the bot from referred users"""
    amount: int
    """Integer amount of Telegram Stars received by the affiliate from the transaction, rounded to 0; can be negative for refunds"""
    nanostar_amount: Optional[int] = Field(default=None)
    """Optional. The number of 1/1000000000 shares of Telegram Stars received by the affiliate; from -999999999 to 999999999; can be negative for refunds"""

class TransactionPartnerUser(_Base, frozen=True):
    """Describes a transaction with a user.
    
    https://core.telegram.org/bots/api#transactionpartneruser
    """
    type: Literal["user"] = Field(default='user')
    """Type of the transaction partner, always "user" """
    transaction_type: str
    """Type of the transaction, currently one of "invoice_payment" for payments via invoices, "paid_media_payment" for payments for paid media, "gift_purchase" for gifts sent by the bot, "premium_purchase" for Telegram Premium subscriptions gifted by the bot, "business_account_transfer" for direct transfers from managed business accounts"""
    user: User
    """Information about the user"""
    affiliate: Optional[AffiliateInfo] = Field(default=None)
    """Optional. Information about the affiliate that received a commission via this transaction. Can be available only for "invoice_payment" and "paid_media_payment" transactions."""
    invoice_payload: Optional[str] = Field(default=None)
    """Optional. Bot-specified invoice payload. Can be available only for "invoice_payment" transactions."""
    subscription_period: Optional[int] = Field(default=None)
    """Optional. The duration of the paid subscription. Can be available only for "invoice_payment" transactions."""
    paid_media: Optional[List[PaidMedia]] = Field(default=None)
    """Optional. Information about the paid media bought by the user; for "paid_media_payment" transactions only"""
    paid_media_payload: Optional[str] = Field(default=None)
    """Optional. Bot-specified paid media payload. Can be available only for "paid_media_payment" transactions."""
    gift: Optional[Gift] = Field(default=None)
    """Optional. The gift sent to the user by the bot; for "gift_purchase" transactions only"""
    premium_subscription_duration: Optional[int] = Field(default=None)
    """Optional. Number of months the gifted Telegram Premium subscription will be active for; for "premium_purchase" transactions only"""

class TransactionPartnerChat(_Base, frozen=True):
    """Describes a transaction with a chat.
    
    https://core.telegram.org/bots/api#transactionpartnerchat
    """
    type: Literal["chat"] = Field(default='chat')
    """Type of the transaction partner, always "chat" """
    chat: Chat
    """Information about the chat"""
    gift: Optional[Gift] = Field(default=None)
    """Optional. The gift sent to the chat by the bot"""

class TransactionPartnerAffiliateProgram(_Base, frozen=True):
    """Describes the affiliate program that issued the affiliate commission received via this transaction.
    
    https://core.telegram.org/bots/api#transactionpartneraffiliateprogram
    """
    type: Literal["affiliate_program"] = Field(default='affiliate_program')
    """Type of the transaction partner, always "affiliate_program" """
    sponsor_user: Optional[User] = Field(default=None)
    """Optional. Information about the bot that sponsored the affiliate program"""
    commission_per_mille: int
    """The number of Telegram Stars received by the bot for each 1000 Telegram Stars received by the affiliate program sponsor from referred users"""

class TransactionPartnerFragment(_Base, frozen=True):
    """Describes a withdrawal transaction with Fragment.
    
    https://core.telegram.org/bots/api#transactionpartnerfragment
    """
    type: Literal["fragment"] = Field(default='fragment')
    """Type of the transaction partner, always "fragment" """
    withdrawal_state: Optional[RevenueWithdrawalState] = Field(default=None)
    """Optional. State of the transaction if the transaction is outgoing"""

class TransactionPartnerTelegramAds(_Base, frozen=True):
    """Describes a withdrawal transaction to the Telegram Ads platform.
    
    https://core.telegram.org/bots/api#transactionpartnertelegramads
    """
    type: Literal["telegram_ads"] = Field(default='telegram_ads')
    """Type of the transaction partner, always "telegram_ads" """

class TransactionPartnerTelegramApi(_Base, frozen=True):
    """Describes a transaction with payment for paid broadcasting.
    
    https://core.telegram.org/bots/api#transactionpartnertelegramapi
    """
    type: Literal["telegram_api"] = Field(default='telegram_api')
    """Type of the transaction partner, always "telegram_api" """
    request_count: int
    """The number of successful requests that exceeded regular limits and were therefore billed"""

class TransactionPartnerOther(_Base, frozen=True):
    """Describes a transaction with an unknown source or recipient.
    
    https://core.telegram.org/bots/api#transactionpartnerother
    """
    type: Literal["other"] = Field(default='other')
    """Type of the transaction partner, always "other" """

class StarTransaction(_Base, frozen=True):
    """Describes a Telegram Star transaction. Note that if the buyer initiates a chargeback with the payment provider from whom they acquired Stars (e.g., Apple, Google) following this transaction, the refunded Stars will be deducted from the bot's balance. This is outside of Telegram's control.
    
    https://core.telegram.org/bots/api#startransaction
    """
    id: str
    """Unique identifier of the transaction. Coincides with the identifier of the original transaction for refund transactions. Coincides with SuccessfulPayment.telegram_payment_charge_id for successful incoming payments from users."""
    amount: int
    """Integer amount of Telegram Stars transferred by the transaction"""
    nanostar_amount: Optional[int] = Field(default=None)
    """Optional. The number of 1/1000000000 shares of Telegram Stars transferred by the transaction; from 0 to 999999999"""
    date: int
    """Date the transaction was created in Unix time"""
    source: Optional[TransactionPartner] = Field(default=None)
    """Optional. Source of an incoming transaction (e.g., a user purchasing goods or services, Fragment refunding a failed withdrawal). Only for incoming transactions."""
    receiver: Optional[TransactionPartner] = Field(default=None)
    """Optional. Receiver of an outgoing transaction (e.g., a user for a purchase refund, Fragment for a withdrawal). Only for outgoing transactions."""

class StarTransactions(_Base, frozen=True):
    """Contains a list of Telegram Star transactions.
    
    https://core.telegram.org/bots/api#startransactions
    """
    transactions: List[StarTransaction]
    """The list of transactions"""

class PassportData(_Base, frozen=True):
    """Describes Telegram Passport data shared with the bot by the user.
    
    https://core.telegram.org/bots/api#passportdata
    """
    data: List[EncryptedPassportElement]
    """Array with information about documents and other Telegram Passport elements that was shared with the bot"""
    credentials: EncryptedCredentials
    """Encrypted credentials required to decrypt the data"""

class PassportFile(_Base, frozen=True):
    """This object represents a file uploaded to Telegram Passport. Currently all Telegram Passport files are in JPEG format when decrypted and don't exceed 10MB.
    
    https://core.telegram.org/bots/api#passportfile
    """
    file_id: str
    """Identifier for this file, which can be used to download or reuse the file"""
    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    file_size: int
    """File size in bytes"""
    file_date: int
    """Unix time when the file was uploaded"""

class EncryptedPassportElement(_Base, frozen=True):
    """Describes documents or other Telegram Passport elements shared with the bot by the user.
    
    https://core.telegram.org/bots/api#encryptedpassportelement
    """
    type: str
    """Element type. One of "personal_details", "passport", "driver_license", "identity_card", "internal_passport", "address", "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration", "phone_number", "email"."""
    data: Optional[str] = Field(default=None)
    """Optional. Base64-encoded encrypted Telegram Passport element data provided by the user; available only for "personal_details", "passport", "driver_license", "identity_card", "internal_passport" and "address" types. Can be decrypted and verified using the accompanying EncryptedCredentials."""
    phone_number: Optional[str] = Field(default=None)
    """Optional. User's verified phone number; available only for "phone_number" type"""
    email: Optional[str] = Field(default=None)
    """Optional. User's verified email address; available only for "email" type"""
    files: Optional[List[PassportFile]] = Field(default=None)
    """Optional. Array of encrypted files with documents provided by the user; available only for "utility_bill", "bank_statement", "rental_agreement", "passport_registration" and "temporary_registration" types. Files can be decrypted and verified using the accompanying EncryptedCredentials."""
    front_side: Optional[PassportFile] = Field(default=None)
    """Optional. Encrypted file with the front side of the document, provided by the user; available only for "passport", "driver_license", "identity_card" and "internal_passport". The file can be decrypted and verified using the accompanying EncryptedCredentials."""
    reverse_side: Optional[PassportFile] = Field(default=None)
    """Optional. Encrypted file with the reverse side of the document, provided by the user; available only for "driver_license" and "identity_card". The file can be decrypted and verified using the accompanying EncryptedCredentials."""
    selfie: Optional[PassportFile] = Field(default=None)
    """Optional. Encrypted file with the selfie of the user holding a document, provided by the user; available if requested for "passport", "driver_license", "identity_card" and "internal_passport". The file can be decrypted and verified using the accompanying EncryptedCredentials."""
    translation: Optional[List[PassportFile]] = Field(default=None)
    """Optional. Array of encrypted files with translated versions of documents provided by the user; available if requested for "passport", "driver_license", "identity_card", "internal_passport", "utility_bill", "bank_statement", "rental_agreement", "passport_registration" and "temporary_registration" types. Files can be decrypted and verified using the accompanying EncryptedCredentials."""
    hash: str
    """Base64-encoded element hash for using in PassportElementErrorUnspecified"""

class EncryptedCredentials(_Base, frozen=True):
    """Describes data required for decrypting and authenticating EncryptedPassportElement. See the Telegram Passport Documentation for a complete description of the data decryption and authentication processes.
    
    https://core.telegram.org/bots/api#encryptedcredentials
    """
    data: str
    """Base64-encoded encrypted JSON-serialized data with unique user's payload, data hashes and secrets required for EncryptedPassportElement decryption and authentication"""
    hash: str
    """Base64-encoded data hash for data authentication"""
    secret: str
    """Base64-encoded secret, encrypted with the bot's public RSA key, required for data decryption"""

class PassportElementErrorDataField(_Base, frozen=True):
    """Represents an issue in one of the data fields that was provided by the user. The error is considered resolved when the field's value changes.
    
    https://core.telegram.org/bots/api#passportelementerrordatafield
    """
    source: Literal["data"] = Field(default='data')
    """Error source, must be data"""
    type: str
    """The section of the user's Telegram Passport which has the error, one of "personal_details", "passport", "driver_license", "identity_card", "internal_passport", "address" """
    field_name: str
    """Name of the data field which has the error"""
    data_hash: str
    """Base64-encoded data hash"""
    message: str
    """Error message"""

class PassportElementErrorFrontSide(_Base, frozen=True):
    """Represents an issue with the front side of a document. The error is considered resolved when the file with the front side of the document changes.
    
    https://core.telegram.org/bots/api#passportelementerrorfrontside
    """
    source: Literal["front_side"] = Field(default='front_side')
    """Error source, must be front_side"""
    type: str
    """The section of the user's Telegram Passport which has the issue, one of "passport", "driver_license", "identity_card", "internal_passport" """
    file_hash: str
    """Base64-encoded hash of the file with the front side of the document"""
    message: str
    """Error message"""

class PassportElementErrorReverseSide(_Base, frozen=True):
    """Represents an issue with the reverse side of a document. The error is considered resolved when the file with reverse side of the document changes.
    
    https://core.telegram.org/bots/api#passportelementerrorreverseside
    """
    source: Literal["reverse_side"] = Field(default='reverse_side')
    """Error source, must be reverse_side"""
    type: str
    """The section of the user's Telegram Passport which has the issue, one of "driver_license", "identity_card" """
    file_hash: str
    """Base64-encoded hash of the file with the reverse side of the document"""
    message: str
    """Error message"""

class PassportElementErrorSelfie(_Base, frozen=True):
    """Represents an issue with the selfie with a document. The error is considered resolved when the file with the selfie changes.
    
    https://core.telegram.org/bots/api#passportelementerrorselfie
    """
    source: Literal["selfie"] = Field(default='selfie')
    """Error source, must be selfie"""
    type: str
    """The section of the user's Telegram Passport which has the issue, one of "passport", "driver_license", "identity_card", "internal_passport" """
    file_hash: str
    """Base64-encoded hash of the file with the selfie"""
    message: str
    """Error message"""

class PassportElementErrorFile(_Base, frozen=True):
    """Represents an issue with a document scan. The error is considered resolved when the file with the document scan changes.
    
    https://core.telegram.org/bots/api#passportelementerrorfile
    """
    source: Literal["file"] = Field(default='file')
    """Error source, must be file"""
    type: str
    """The section of the user's Telegram Passport which has the issue, one of "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration" """
    file_hash: str
    """Base64-encoded file hash"""
    message: str
    """Error message"""

class PassportElementErrorFiles(_Base, frozen=True):
    """Represents an issue with a list of scans. The error is considered resolved when the list of files containing the scans changes.
    
    https://core.telegram.org/bots/api#passportelementerrorfiles
    """
    source: Literal["files"] = Field(default='files')
    """Error source, must be files"""
    type: str
    """The section of the user's Telegram Passport which has the issue, one of "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration" """
    file_hashes: List[str]
    """List of base64-encoded file hashes"""
    message: str
    """Error message"""

class PassportElementErrorTranslationFile(_Base, frozen=True):
    """Represents an issue with one of the files that constitute the translation of a document. The error is considered resolved when the file changes.
    
    https://core.telegram.org/bots/api#passportelementerrortranslationfile
    """
    source: Literal["translation_file"] = Field(default='translation_file')
    """Error source, must be translation_file"""
    type: str
    """Type of element of the user's Telegram Passport which has the issue, one of "passport", "driver_license", "identity_card", "internal_passport", "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration" """
    file_hash: str
    """Base64-encoded file hash"""
    message: str
    """Error message"""

class PassportElementErrorTranslationFiles(_Base, frozen=True):
    """Represents an issue with the translated version of a document. The error is considered resolved when a file with the document translation change.
    
    https://core.telegram.org/bots/api#passportelementerrortranslationfiles
    """
    source: Literal["translation_files"] = Field(default='translation_files')
    """Error source, must be translation_files"""
    type: str
    """Type of element of the user's Telegram Passport which has the issue, one of "passport", "driver_license", "identity_card", "internal_passport", "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration" """
    file_hashes: List[str]
    """List of base64-encoded file hashes"""
    message: str
    """Error message"""

class PassportElementErrorUnspecified(_Base, frozen=True):
    """Represents an issue in an unspecified place. The error is considered resolved when new data is added.
    
    https://core.telegram.org/bots/api#passportelementerrorunspecified
    """
    source: Literal["unspecified"] = Field(default='unspecified')
    """Error source, must be unspecified"""
    type: str
    """Type of element of the user's Telegram Passport which has the issue"""
    element_hash: str
    """Base64-encoded element hash"""
    message: str
    """Error message"""

class Game(_Base, frozen=True):
    """This object represents a game. Use BotFather to create and edit games, their short names will act as unique identifiers.
    
    https://core.telegram.org/bots/api#game
    """
    title: str
    """Title of the game"""
    description: str
    """Description of the game"""
    photo: List[PhotoSize]
    """Photo that will be displayed in the game message in chats"""
    text: Optional[str] = Field(default=None)
    """Optional. Brief description of the game or high scores included in the game message. Can be automatically edited to include current high scores for the game when the bot calls setGameScore, or manually edited using editMessageText. 0-4096 characters."""
    text_entities: Optional[List[MessageEntity]] = Field(default=None)
    """Optional. Special entities that appear in text, such as usernames, URLs, bot commands, etc."""
    animation: Optional[Animation] = Field(default=None)
    """Optional. Animation that will be displayed in the game message in chats. Upload via BotFather."""

class CallbackGame(_Base, frozen=True):
    """A placeholder, currently holds no information. Use BotFather to set up your game.
    
    https://core.telegram.org/bots/api#callbackgame
    """

class GameHighScore(_Base, frozen=True):
    """This object represents one row of the high scores table for a game.
    
    https://core.telegram.org/bots/api#gamehighscore
    """
    position: int
    """Position in high score table for the game"""
    user: User
    """User"""
    score: int
    """Score"""


def _maybe_inaccessible_tag(value: Any) -> str:
    date = value.get("date") if isinstance(value, dict) else getattr(value, "date", None)
    return "inaccessible" if date == 0 else "message"

MaybeInaccessibleMessage = Annotated[
    Union[
        Annotated[Message, Tag("message")],
        Annotated[InaccessibleMessage, Tag("inaccessible")],
    ],
    Discriminator(_maybe_inaccessible_tag),
]
MessageOrigin = Annotated[Union[MessageOriginUser, MessageOriginHiddenUser, MessageOriginChat, MessageOriginChannel], Field(discriminator="type")]
PaidMedia = Annotated[Union[PaidMediaLivePhoto, PaidMediaPhoto, PaidMediaPreview, PaidMediaVideo], Field(discriminator="type")]
InputPollMedia = Annotated[Union[InputMediaAnimation, InputMediaAudio, InputMediaDocument, InputMediaLivePhoto, InputMediaLocation, InputMediaPhoto, InputMediaVenue, InputMediaVideo], Field(discriminator="type")]
InputPollOptionMedia = Annotated[Union[InputMediaAnimation, InputMediaLink, InputMediaLivePhoto, InputMediaLocation, InputMediaPhoto, InputMediaSticker, InputMediaVenue, InputMediaVideo], Field(discriminator="type")]
BackgroundFill = Annotated[Union[BackgroundFillSolid, BackgroundFillGradient, BackgroundFillFreeformGradient], Field(discriminator="type")]
BackgroundType = Annotated[Union[BackgroundTypeFill, BackgroundTypeWallpaper, BackgroundTypePattern, BackgroundTypeChatTheme], Field(discriminator="type")]
ChatMember = Annotated[Union[ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMemberRestricted, ChatMemberLeft, ChatMemberBanned], Field(discriminator="status")]
StoryAreaType = Annotated[Union[StoryAreaTypeLocation, StoryAreaTypeSuggestedReaction, StoryAreaTypeLink, StoryAreaTypeWeather, StoryAreaTypeUniqueGift], Field(discriminator="type")]
ReactionType = Annotated[Union[ReactionTypeEmoji, ReactionTypeCustomEmoji, ReactionTypePaid], Field(discriminator="type")]
OwnedGift = Annotated[Union[OwnedGiftRegular, OwnedGiftUnique], Field(discriminator="type")]
BotCommandScope = Annotated[Union[BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, BotCommandScopeAllChatAdministrators, BotCommandScopeChat, BotCommandScopeChatAdministrators, BotCommandScopeChatMember], Field(discriminator="type")]
MenuButton = Annotated[Union[MenuButtonCommands, MenuButtonWebApp, MenuButtonDefault], Field(discriminator="type")]
ChatBoostSource = Annotated[Union[ChatBoostSourcePremium, ChatBoostSourceGiftCode, ChatBoostSourceGiveaway], Field(discriminator="source")]
InputMedia = Annotated[Union[InputMediaAnimation, InputMediaAudio, InputMediaDocument, InputMediaLivePhoto, InputMediaPhoto, InputMediaVideo], Field(discriminator="type")]
InputPaidMedia = Annotated[Union[InputPaidMediaLivePhoto, InputPaidMediaPhoto, InputPaidMediaVideo], Field(discriminator="type")]
InputProfilePhoto = Annotated[Union[InputProfilePhotoStatic, InputProfilePhotoAnimated], Field(discriminator="type")]
InputStoryContent = Annotated[Union[InputStoryContentPhoto, InputStoryContentVideo], Field(discriminator="type")]
RichBlock = Annotated[Union[RichBlockParagraph, RichBlockSectionHeading, RichBlockPreformatted, RichBlockFooter, RichBlockDivider, RichBlockMathematicalExpression, RichBlockAnchor, RichBlockList, RichBlockBlockQuotation, RichBlockExpandableBlockQuotation, RichBlockPullQuotation, RichBlockCollage, RichBlockSlideshow, RichBlockTable, RichBlockDetails, RichBlockMap, RichBlockButtons, RichBlockAnimation, RichBlockAudio, RichBlockDocument, RichBlockPhoto, RichBlockVideo, RichBlockVoiceNote, RichBlockThinking], Field(discriminator="type")]
InputRichBlock = Annotated[Union[InputRichBlockParagraph, InputRichBlockSectionHeading, InputRichBlockPreformatted, InputRichBlockFooter, InputRichBlockDivider, InputRichBlockMathematicalExpression, InputRichBlockAnchor, InputRichBlockList, InputRichBlockBlockQuotation, InputRichBlockExpandableBlockQuotation, InputRichBlockPullQuotation, InputRichBlockCollage, InputRichBlockSlideshow, InputRichBlockTable, InputRichBlockDetails, InputRichBlockMap, InputRichBlockButtons, InputRichBlockAnimation, InputRichBlockAudio, InputRichBlockDocument, InputRichBlockPhoto, InputRichBlockVideo, InputRichBlockVoiceNote, InputRichBlockThinking], Field(discriminator="type")]
InlineQueryResult = Union[InlineQueryResultCachedAudio, InlineQueryResultCachedDocument, InlineQueryResultCachedGif, InlineQueryResultCachedMpeg4Gif, InlineQueryResultCachedPhoto, InlineQueryResultCachedSticker, InlineQueryResultCachedVideo, InlineQueryResultCachedVoice, InlineQueryResultArticle, InlineQueryResultAudio, InlineQueryResultContact, InlineQueryResultGame, InlineQueryResultDocument, InlineQueryResultGif, InlineQueryResultLocation, InlineQueryResultMpeg4Gif, InlineQueryResultPhoto, InlineQueryResultVenue, InlineQueryResultVideo, InlineQueryResultVoice]
InputMessageContent = Union[InputTextMessageContent, InputRichMessageContent, InputLocationMessageContent, InputVenueMessageContent, InputContactMessageContent, InputInvoiceMessageContent]
RevenueWithdrawalState = Annotated[Union[RevenueWithdrawalStatePending, RevenueWithdrawalStateSucceeded, RevenueWithdrawalStateFailed], Field(discriminator="type")]
TransactionPartner = Annotated[Union[TransactionPartnerUser, TransactionPartnerChat, TransactionPartnerAffiliateProgram, TransactionPartnerFragment, TransactionPartnerTelegramAds, TransactionPartnerTelegramApi, TransactionPartnerOther], Field(discriminator="type")]
PassportElementError = Annotated[Union[PassportElementErrorDataField, PassportElementErrorFrontSide, PassportElementErrorReverseSide, PassportElementErrorSelfie, PassportElementErrorFile, PassportElementErrorFiles, PassportElementErrorTranslationFile, PassportElementErrorTranslationFiles, PassportElementErrorUnspecified], Field(discriminator="source")]


__all__ = [
    "Update",
    "WebhookInfo",
    "User",
    "Chat",
    "ChatFullInfo",
    "Message",
    "MessageId",
    "InaccessibleMessage",
    "MaybeInaccessibleMessage",
    "MessageEntity",
    "TextQuote",
    "ExternalReplyInfo",
    "ReplyParameters",
    "EphemeralMessageParameters",
    "MessageOrigin",
    "MessageOriginUser",
    "MessageOriginHiddenUser",
    "MessageOriginChat",
    "MessageOriginChannel",
    "PhotoSize",
    "Animation",
    "Audio",
    "Document",
    "LivePhoto",
    "Story",
    "VideoQuality",
    "Video",
    "VideoNote",
    "Voice",
    "PaidMediaInfo",
    "PaidMedia",
    "PaidMediaLivePhoto",
    "PaidMediaPhoto",
    "PaidMediaPreview",
    "PaidMediaVideo",
    "Contact",
    "Dice",
    "Link",
    "PollMedia",
    "InputPollMedia",
    "InputPollOptionMedia",
    "PollOption",
    "InputPollOption",
    "PollAnswer",
    "Poll",
    "ChecklistTask",
    "Checklist",
    "InputChecklistTask",
    "InputChecklist",
    "Location",
    "Venue",
    "WebAppData",
    "ProximityAlertTriggered",
    "MessageAutoDeleteTimerChanged",
    "ManagedBotCreated",
    "ManagedBotUpdated",
    "BotSubscriptionUpdated",
    "MessageGenerationStopped",
    "PollOptionAdded",
    "PollOptionDeleted",
    "ChatBoostAdded",
    "BackgroundFill",
    "BackgroundFillSolid",
    "BackgroundFillGradient",
    "BackgroundFillFreeformGradient",
    "BackgroundType",
    "BackgroundTypeFill",
    "BackgroundTypeWallpaper",
    "BackgroundTypePattern",
    "BackgroundTypeChatTheme",
    "ChatBackground",
    "ChecklistTasksDone",
    "ChecklistTasksAdded",
    "CommunityChatAdded",
    "CommunityChatJoined",
    "CommunityChatRemoved",
    "ForumTopicCreated",
    "ForumTopicClosed",
    "ForumTopicEdited",
    "ForumTopicReopened",
    "GeneralForumTopicHidden",
    "GeneralForumTopicUnhidden",
    "SharedUser",
    "UsersShared",
    "ChatShared",
    "WriteAccessAllowed",
    "VideoChatScheduled",
    "VideoChatStarted",
    "VideoChatEnded",
    "VideoChatParticipantsInvited",
    "PaidMessagePriceChanged",
    "DirectMessagePriceChanged",
    "SuggestedPostApproved",
    "SuggestedPostApprovalFailed",
    "SuggestedPostDeclined",
    "SuggestedPostPaid",
    "SuggestedPostRefunded",
    "GiveawayCreated",
    "Giveaway",
    "GiveawayWinners",
    "GiveawayCompleted",
    "LinkPreviewOptions",
    "SuggestedPostPrice",
    "SuggestedPostInfo",
    "SuggestedPostParameters",
    "DirectMessagesTopic",
    "UserProfilePhotos",
    "UserProfileAudios",
    "File",
    "WebAppInfo",
    "ReplyKeyboardMarkup",
    "KeyboardButton",
    "KeyboardButtonRequestUsers",
    "KeyboardButtonRequestChat",
    "KeyboardButtonRequestManagedBot",
    "KeyboardButtonPollType",
    "ReplyKeyboardRemove",
    "InlineKeyboardMarkup",
    "InlineKeyboardButton",
    "LoginUrl",
    "SwitchInlineQueryChosenChat",
    "CopyTextButton",
    "DisabledButton",
    "CallbackQuery",
    "ForceReply",
    "Community",
    "ChatPhoto",
    "ChatInviteLink",
    "ChatAdministratorRights",
    "ChatMemberUpdated",
    "ChatMember",
    "ChatMemberOwner",
    "ChatMemberAdministrator",
    "ChatMemberMember",
    "ChatMemberRestricted",
    "ChatMemberLeft",
    "ChatMemberBanned",
    "ChatJoinRequest",
    "ChatPermissions",
    "Birthdate",
    "BusinessIntro",
    "BusinessLocation",
    "BusinessOpeningHoursInterval",
    "BusinessOpeningHours",
    "UserRating",
    "StoryAreaPosition",
    "LocationAddress",
    "StoryAreaType",
    "StoryAreaTypeLocation",
    "StoryAreaTypeSuggestedReaction",
    "StoryAreaTypeLink",
    "StoryAreaTypeWeather",
    "StoryAreaTypeUniqueGift",
    "StoryArea",
    "ChatLocation",
    "ReactionType",
    "ReactionTypeEmoji",
    "ReactionTypeCustomEmoji",
    "ReactionTypePaid",
    "ReactionCount",
    "MessageReactionUpdated",
    "MessageReactionCountUpdated",
    "ForumTopic",
    "GiftBackground",
    "Gift",
    "Gifts",
    "UniqueGiftModel",
    "UniqueGiftSymbol",
    "UniqueGiftBackdropColors",
    "UniqueGiftBackdrop",
    "UniqueGiftColors",
    "UniqueGift",
    "GiftInfo",
    "UniqueGiftInfo",
    "OwnedGift",
    "OwnedGiftRegular",
    "OwnedGiftUnique",
    "OwnedGifts",
    "BotAccessSettings",
    "AcceptedGiftTypes",
    "StarAmount",
    "BotCommand",
    "BotCommandScope",
    "BotCommandScopeDefault",
    "BotCommandScopeAllPrivateChats",
    "BotCommandScopeAllGroupChats",
    "BotCommandScopeAllChatAdministrators",
    "BotCommandScopeChat",
    "BotCommandScopeChatAdministrators",
    "BotCommandScopeChatMember",
    "BotName",
    "BotDescription",
    "BotShortDescription",
    "MenuButton",
    "MenuButtonCommands",
    "MenuButtonWebApp",
    "MenuButtonDefault",
    "ChatBoostSource",
    "ChatBoostSourcePremium",
    "ChatBoostSourceGiftCode",
    "ChatBoostSourceGiveaway",
    "ChatBoost",
    "ChatBoostUpdated",
    "ChatBoostRemoved",
    "ChatOwnerLeft",
    "ChatOwnerChanged",
    "UserChatBoosts",
    "BusinessBotRights",
    "BusinessConnection",
    "BusinessMessagesDeleted",
    "SentWebAppMessage",
    "SentGuestMessage",
    "PreparedInlineMessage",
    "PreparedKeyboardButton",
    "ResponseParameters",
    "InputMedia",
    "InputMediaAnimation",
    "InputMediaAudio",
    "InputMediaDocument",
    "InputMediaLink",
    "InputMediaLivePhoto",
    "InputMediaLocation",
    "InputMediaPhoto",
    "InputMediaSticker",
    "InputMediaVenue",
    "InputMediaVideo",
    "InputMediaVoiceNote",
    "InputPaidMedia",
    "InputPaidMediaLivePhoto",
    "InputPaidMediaPhoto",
    "InputPaidMediaVideo",
    "InputProfilePhoto",
    "InputProfilePhotoStatic",
    "InputProfilePhotoAnimated",
    "InputStoryContent",
    "InputStoryContentPhoto",
    "InputStoryContentVideo",
    "Sticker",
    "StickerSet",
    "MaskPosition",
    "InputSticker",
    "RichMessage",
    "InputRichMessage",
    "InputRichMessageMedia",
    "RichMessageButton",
    "RichText",
    "RichTextBold",
    "RichTextItalic",
    "RichTextUnderline",
    "RichTextStrikethrough",
    "RichTextSpoiler",
    "RichTextDateTime",
    "RichTextTextMention",
    "RichTextSubscript",
    "RichTextSuperscript",
    "RichTextMarked",
    "RichTextCode",
    "RichTextCustomEmoji",
    "RichTextMathematicalExpression",
    "RichTextUrl",
    "RichTextEmailAddress",
    "RichTextPhoneNumber",
    "RichTextBankCardNumber",
    "RichTextMention",
    "RichTextHashtag",
    "RichTextCashtag",
    "RichTextBotCommand",
    "RichTextButton",
    "RichTextAnchor",
    "RichTextAnchorLink",
    "RichTextReference",
    "RichTextReferenceLink",
    "RichBlockCaption",
    "RichBlockTableCell",
    "RichBlockListItem",
    "RichBlock",
    "RichBlockParagraph",
    "RichBlockSectionHeading",
    "RichBlockPreformatted",
    "RichBlockFooter",
    "RichBlockDivider",
    "RichBlockMathematicalExpression",
    "RichBlockAnchor",
    "RichBlockList",
    "RichBlockBlockQuotation",
    "RichBlockExpandableBlockQuotation",
    "RichBlockPullQuotation",
    "RichBlockCollage",
    "RichBlockSlideshow",
    "RichBlockTable",
    "RichBlockDetails",
    "RichBlockMap",
    "RichBlockButtons",
    "RichBlockAnimation",
    "RichBlockAudio",
    "RichBlockDocument",
    "RichBlockPhoto",
    "RichBlockVideo",
    "RichBlockVoiceNote",
    "RichBlockThinking",
    "InputRichBlockListItem",
    "InputRichBlock",
    "InputRichBlockParagraph",
    "InputRichBlockSectionHeading",
    "InputRichBlockPreformatted",
    "InputRichBlockFooter",
    "InputRichBlockDivider",
    "InputRichBlockMathematicalExpression",
    "InputRichBlockAnchor",
    "InputRichBlockList",
    "InputRichBlockBlockQuotation",
    "InputRichBlockExpandableBlockQuotation",
    "InputRichBlockPullQuotation",
    "InputRichBlockCollage",
    "InputRichBlockSlideshow",
    "InputRichBlockTable",
    "InputRichBlockDetails",
    "InputRichBlockMap",
    "InputRichBlockButtons",
    "InputRichBlockAnimation",
    "InputRichBlockAudio",
    "InputRichBlockDocument",
    "InputRichBlockPhoto",
    "InputRichBlockVideo",
    "InputRichBlockVoiceNote",
    "InputRichBlockThinking",
    "InlineQuery",
    "InlineQueryResultsButton",
    "InlineQueryResult",
    "InlineQueryResultArticle",
    "InlineQueryResultPhoto",
    "InlineQueryResultGif",
    "InlineQueryResultMpeg4Gif",
    "InlineQueryResultVideo",
    "InlineQueryResultAudio",
    "InlineQueryResultVoice",
    "InlineQueryResultDocument",
    "InlineQueryResultLocation",
    "InlineQueryResultVenue",
    "InlineQueryResultContact",
    "InlineQueryResultGame",
    "InlineQueryResultCachedPhoto",
    "InlineQueryResultCachedGif",
    "InlineQueryResultCachedMpeg4Gif",
    "InlineQueryResultCachedSticker",
    "InlineQueryResultCachedDocument",
    "InlineQueryResultCachedVideo",
    "InlineQueryResultCachedVoice",
    "InlineQueryResultCachedAudio",
    "InputMessageContent",
    "InputTextMessageContent",
    "InputRichMessageContent",
    "InputLocationMessageContent",
    "InputVenueMessageContent",
    "InputContactMessageContent",
    "InputInvoiceMessageContent",
    "ChosenInlineResult",
    "LabeledPrice",
    "Invoice",
    "ShippingAddress",
    "OrderInfo",
    "ShippingOption",
    "SuccessfulPayment",
    "RefundedPayment",
    "ShippingQuery",
    "PreCheckoutQuery",
    "PaidMediaPurchased",
    "RevenueWithdrawalState",
    "RevenueWithdrawalStatePending",
    "RevenueWithdrawalStateSucceeded",
    "RevenueWithdrawalStateFailed",
    "AffiliateInfo",
    "TransactionPartner",
    "TransactionPartnerUser",
    "TransactionPartnerChat",
    "TransactionPartnerAffiliateProgram",
    "TransactionPartnerFragment",
    "TransactionPartnerTelegramAds",
    "TransactionPartnerTelegramApi",
    "TransactionPartnerOther",
    "StarTransaction",
    "StarTransactions",
    "PassportData",
    "PassportFile",
    "EncryptedPassportElement",
    "EncryptedCredentials",
    "PassportElementError",
    "PassportElementErrorDataField",
    "PassportElementErrorFrontSide",
    "PassportElementErrorReverseSide",
    "PassportElementErrorSelfie",
    "PassportElementErrorFile",
    "PassportElementErrorFiles",
    "PassportElementErrorTranslationFile",
    "PassportElementErrorTranslationFiles",
    "PassportElementErrorUnspecified",
    "Game",
    "CallbackGame",
    "GameHighScore",
]

for _name in __all__:
    _model = globals()[_name]
    if isinstance(_model, type):
        _model.model_rebuild()
