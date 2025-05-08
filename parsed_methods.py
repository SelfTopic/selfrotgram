
# class: start
from typing import ClassVar
from .base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetMe(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMe"
# class: end

# class: start
from typing import ClassVar
from .base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class LogOut(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "logOut"
# class: end

# class: start
from typing import ClassVar
from .base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class Close(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "close"
# class: end

# class: start
@dataclass
class SendMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendMessage"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    text: str
    parse_mode: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class ForwardMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "forwardMessage"
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    from_chat_id: Union[int, str]
    video_start_timestamp: Optional[int] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    message_id: int
# class: end

# class: start
@dataclass
class ForwardMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "forwardMessages"
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    from_chat_id: Union[int, str]
    message_ids: List[int]
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
# class: end

# class: start
@dataclass
class CopyMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "copyMessage"
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    from_chat_id: Union[int, str]
    message_id: int
    video_start_timestamp: Optional[int] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class CopyMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "copyMessages"
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    from_chat_id: Union[int, str]
    message_ids: List[int]
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    remove_caption: Optional[bool] = None
# class: end

# class: start
@dataclass
class SendPhoto(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendPhoto"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    photo: Union[InputFile, str]
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    has_spoiler: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendAudio(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendAudio"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    audio: Union[InputFile, str]
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    duration: Optional[int] = None
    performer: Optional[str] = None
    title: Optional[str] = None
    thumbnail: Optional[Union[InputFile, str]] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendDocument(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendDocument"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    document: Union[InputFile, str]
    thumbnail: Optional[Union[InputFile, str]] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    disable_content_type_detection: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendVideo(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendVideo"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    video: Union[InputFile, str]
    duration: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    thumbnail: Optional[Union[InputFile, str]] = None
    cover: Optional[Union[InputFile, str]] = None
    start_timestamp: Optional[int] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    has_spoiler: Optional[bool] = None
    supports_streaming: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendAnimation(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendAnimation"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    animation: Union[InputFile, str]
    duration: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    thumbnail: Optional[Union[InputFile, str]] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    has_spoiler: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendVoice(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendVoice"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    voice: Union[InputFile, str]
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    duration: Optional[int] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendVideoNote(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendVideoNote"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    video_note: Union[InputFile, str]
    duration: Optional[int] = None
    length: Optional[int] = None
    thumbnail: Optional[Union[InputFile, str]] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendPaidMedia(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendPaidMedia"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    star_count: int
    media: List[InputPaidMedia]
    payload: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendMediaGroup(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendMediaGroup"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    media: List[InputMediaAudio, InputMediaDocument, InputMediaPhoto and InputMediaVideo]
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
# class: end

# class: start
@dataclass
class SendLocation(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendLocation"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    latitude: float
    longitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendVenue(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendVenue"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendContact(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendContact"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    vcard: Optional[str] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendPoll(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendPoll"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    question: str
    question_parse_mode: Optional[str] = None
    question_entities: Optional[List[MessageEntity]] = None
    options: List[InputPollOption]
    is_anonymous: Optional[bool] = None
    type: Optional[str] = None
    allows_multiple_answers: Optional[bool] = None
    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None
    explanation_parse_mode: Optional[str] = None
    explanation_entities: Optional[List[MessageEntity]] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None
    is_closed: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendDice(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendDice"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    emoji: Optional[str] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
# class: end

# class: start
@dataclass
class SendChatAction(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendChatAction"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    action: str
# class: end

# class: start
@dataclass
class SetMessageReaction(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMessageReaction"
    chat_id: Union[int, str]
    message_id: int
    reaction: Optional[List[ReactionType]] = None
    is_big: Optional[bool] = None
# class: end

# class: start
@dataclass
class GetUserProfilePhotos(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getUserProfilePhotos"
    user_id: int
    offset: Optional[int] = None
    limit: Optional[int] = None
# class: end

# class: start
@dataclass
class SetUserEmojiStatus(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setUserEmojiStatus"
    user_id: int
    emoji_status_custom_emoji_id: Optional[str] = None
    emoji_status_expiration_date: Optional[int] = None
# class: end

# class: start
@dataclass
class GetFile(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getFile"
    file_id: str
# class: end

# class: start
@dataclass
class BanChatMember(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "banChatMember"
    chat_id: Union[int, str]
    user_id: int
    until_date: Optional[int] = None
    revoke_messages: Optional[bool] = None
# class: end

# class: start
@dataclass
class UnbanChatMember(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unbanChatMember"
    chat_id: Union[int, str]
    user_id: int
    only_if_banned: Optional[bool] = None
# class: end

# class: start
@dataclass
class RestrictChatMember(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "restrictChatMember"
    chat_id: Union[int, str]
    user_id: int
    permissions: ChatPermissions
    use_independent_chat_permissions: Optional[bool] = None
    until_date: Optional[int] = None
# class: end

# class: start
@dataclass
class PromoteChatMember(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "promoteChatMember"
    chat_id: Union[int, str]
    user_id: int
    is_anonymous: Optional[bool] = None
    can_manage_chat: Optional[bool] = None
    can_delete_messages: Optional[bool] = None
    can_manage_video_chats: Optional[bool] = None
    can_restrict_members: Optional[bool] = None
    can_promote_members: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_post_stories: Optional[bool] = None
    can_edit_stories: Optional[bool] = None
    can_delete_stories: Optional[bool] = None
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
# class: end

# class: start
@dataclass
class SetChatAdministratorCustomTitle(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatAdministratorCustomTitle"
    chat_id: Union[int, str]
    user_id: int
    custom_title: str
# class: end

# class: start
@dataclass
class BanChatSenderChat(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "banChatSenderChat"
    chat_id: Union[int, str]
    sender_chat_id: int
# class: end

# class: start
@dataclass
class UnbanChatSenderChat(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unbanChatSenderChat"
    chat_id: Union[int, str]
    sender_chat_id: int
# class: end

# class: start
@dataclass
class SetChatPermissions(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatPermissions"
    chat_id: Union[int, str]
    permissions: ChatPermissions
    use_independent_chat_permissions: Optional[bool] = None
# class: end

# class: start
@dataclass
class ExportChatInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "exportChatInviteLink"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class CreateChatInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "createChatInviteLink"
    chat_id: Union[int, str]
    name: Optional[str] = None
    expire_date: Optional[int] = None
    member_limit: Optional[int] = None
    creates_join_request: Optional[bool] = None
# class: end

# class: start
@dataclass
class EditChatInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editChatInviteLink"
    chat_id: Union[int, str]
    invite_link: str
    name: Optional[str] = None
    expire_date: Optional[int] = None
    member_limit: Optional[int] = None
    creates_join_request: Optional[bool] = None
# class: end

# class: start
@dataclass
class CreateChatSubscriptionInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "createChatSubscriptionInviteLink"
    chat_id: Union[int, str]
    name: Optional[str] = None
    subscription_period: int
    subscription_price: int
# class: end

# class: start
@dataclass
class EditChatSubscriptionInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editChatSubscriptionInviteLink"
    chat_id: Union[int, str]
    invite_link: str
    name: Optional[str] = None
# class: end

# class: start
@dataclass
class RevokeChatInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "revokeChatInviteLink"
    chat_id: Union[int, str]
    invite_link: str
# class: end

# class: start
@dataclass
class ApproveChatJoinRequest(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "approveChatJoinRequest"
    chat_id: Union[int, str]
    user_id: int
# class: end

# class: start
@dataclass
class DeclineChatJoinRequest(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "declineChatJoinRequest"
    chat_id: Union[int, str]
    user_id: int
# class: end

# class: start
@dataclass
class SetChatPhoto(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatPhoto"
    chat_id: Union[int, str]
    photo: InputFile
# class: end

# class: start
@dataclass
class DeleteChatPhoto(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteChatPhoto"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class SetChatTitle(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatTitle"
    chat_id: Union[int, str]
    title: str
# class: end

# class: start
@dataclass
class SetChatDescription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatDescription"
    chat_id: Union[int, str]
    description: Optional[str] = None
# class: end

# class: start
@dataclass
class PinChatMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "pinChatMessage"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_id: int
    disable_notification: Optional[bool] = None
# class: end

# class: start
@dataclass
class UnpinChatMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unpinChatMessage"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_id: Optional[int] = None
# class: end

# class: start
@dataclass
class UnpinAllChatMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unpinAllChatMessages"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class LeaveChat(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "leaveChat"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class GetChat(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getChat"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class GetChatAdministrators(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getChatAdministrators"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class GetChatMemberCount(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getChatMemberCount"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class GetChatMember(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getChatMember"
    chat_id: Union[int, str]
    user_id: int
# class: end

# class: start
@dataclass
class SetChatStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatStickerSet"
    chat_id: Union[int, str]
    sticker_set_name: str
# class: end

# class: start
@dataclass
class DeleteChatStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteChatStickerSet"
    chat_id: Union[int, str]
# class: end

# class: start
from typing import ClassVar
from .base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetForumTopicIconStickers(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getForumTopicIconStickers"
# class: end

# class: start
@dataclass
class CreateForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "createForumTopic"
    chat_id: Union[int, str]
    name: str
    icon_color: Optional[int] = None
    icon_custom_emoji_id: Optional[str] = None
# class: end

# class: start
@dataclass
class EditForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editForumTopic"
    chat_id: Union[int, str]
    message_thread_id: int
    name: Optional[str] = None
    icon_custom_emoji_id: Optional[str] = None
# class: end

# class: start
@dataclass
class CloseForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "closeForumTopic"
    chat_id: Union[int, str]
    message_thread_id: int
# class: end

# class: start
@dataclass
class ReopenForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "reopenForumTopic"
    chat_id: Union[int, str]
    message_thread_id: int
# class: end

# class: start
@dataclass
class DeleteForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteForumTopic"
    chat_id: Union[int, str]
    message_thread_id: int
# class: end

# class: start
@dataclass
class UnpinAllForumTopicMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unpinAllForumTopicMessages"
    chat_id: Union[int, str]
    message_thread_id: int
# class: end

# class: start
@dataclass
class EditGeneralForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editGeneralForumTopic"
    chat_id: Union[int, str]
    name: str
# class: end

# class: start
@dataclass
class CloseGeneralForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "closeGeneralForumTopic"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class ReopenGeneralForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "reopenGeneralForumTopic"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class HideGeneralForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "hideGeneralForumTopic"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class UnhideGeneralForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unhideGeneralForumTopic"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class UnpinAllGeneralForumTopicMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unpinAllGeneralForumTopicMessages"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class AnswerCallbackQuery(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "answerCallbackQuery"
    callback_query_id: str
    text: Optional[str] = None
    show_alert: Optional[bool] = None
    url: Optional[str] = None
    cache_time: Optional[int] = None
# class: end

# class: start
@dataclass
class GetUserChatBoosts(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getUserChatBoosts"
    chat_id: Union[int, str]
    user_id: int
# class: end

# class: start
@dataclass
class GetBusinessConnection(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getBusinessConnection"
    business_connection_id: str
# class: end

# class: start
@dataclass
class SetMyCommands(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMyCommands"
    commands: List[BotCommand]
    scope: Optional[BotCommandScope] = None
    language_code: Optional[str] = None
# class: end

# class: start
@dataclass
class DeleteMyCommands(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteMyCommands"
    scope: Optional[BotCommandScope] = None
    language_code: Optional[str] = None
# class: end

# class: start
@dataclass
class GetMyCommands(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMyCommands"
    scope: Optional[BotCommandScope] = None
    language_code: Optional[str] = None
# class: end

# class: start
@dataclass
class SetMyName(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMyName"
    name: Optional[str] = None
    language_code: Optional[str] = None
# class: end

# class: start
@dataclass
class GetMyName(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMyName"
    language_code: Optional[str] = None
# class: end

# class: start
@dataclass
class SetMyDescription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMyDescription"
    description: Optional[str] = None
    language_code: Optional[str] = None
# class: end

# class: start
@dataclass
class GetMyDescription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMyDescription"
    language_code: Optional[str] = None
# class: end

# class: start
@dataclass
class SetMyShortDescription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMyShortDescription"
    short_description: Optional[str] = None
    language_code: Optional[str] = None
# class: end

# class: start
@dataclass
class GetMyShortDescription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMyShortDescription"
    language_code: Optional[str] = None
# class: end

# class: start
@dataclass
class SetChatMenuButton(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatMenuButton"
    chat_id: Optional[int] = None
    menu_button: Optional[MenuButton] = None
# class: end

# class: start
@dataclass
class GetChatMenuButton(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getChatMenuButton"
    chat_id: Optional[int] = None
# class: end

# class: start
@dataclass
class SetMyDefaultAdministratorRights(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMyDefaultAdministratorRights"
    rights: Optional[Union[ChatAdministratorRights]] = None
    for_channels: Optional[bool] = None
# class: end

# class: start
@dataclass
class GetMyDefaultAdministratorRights(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMyDefaultAdministratorRights"
    for_channels: Optional[bool] = None
# class: end
