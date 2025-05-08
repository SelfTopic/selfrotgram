
# class: start
class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None
    can_connect_to_business: Optional[bool] = None
    has_main_web_app: Optional[bool] = None
# class: end

# class: start
class Chat(BaseModel):
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[bool] = None
# class: end

# class: start
class ChatFullInfo(BaseModel):
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[bool] = None
    accent_color_id: int
    max_reaction_count: int
    photo: Optional[ChatPhoto] = None
    active_usernames: Optional[List[str]] = None
    birthdate: Optional[Birthdate] = None
    business_intro: Optional[BusinessIntro] = None
    business_location: Optional[BusinessLocation] = None
    business_opening_hours: Optional[BusinessOpeningHours] = None
    personal_chat: Optional[Chat] = None
    available_reactions: Optional[List[ReactionType]] = None
    background_custom_emoji_id: Optional[str] = None
    profile_accent_color_id: Optional[int] = None
    profile_background_custom_emoji_id: Optional[str] = None
    emoji_status_custom_emoji_id: Optional[str] = None
    emoji_status_expiration_date: Optional[int] = None
    bio: Optional[str] = None
    has_private_forwards: Optional[bool] = None
    has_restricted_voice_and_video_messages: Optional[bool] = None
    join_to_send_messages: Optional[bool] = None
    join_by_request: Optional[bool] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional[Message] = None
    permissions: Optional[ChatPermissions] = None
    accepted_gift_types: AcceptedGiftTypes
    can_send_paid_media: Optional[bool] = None
    slow_mode_delay: Optional[int] = None
    unrestrict_boost_count: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_aggressive_anti_spam_enabled: Optional[bool] = None
    has_hidden_members: Optional[bool] = None
    has_protected_content: Optional[bool] = None
    has_visible_history: Optional[bool] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None
    custom_emoji_sticker_set_name: Optional[str] = None
    linked_chat_id: Optional[int] = None
    location: Optional[ChatLocation] = None
# class: end

# class: start
class Message(BaseModel):
    message_id: int
    message_thread_id: Optional[int] = None
    user: Optional[User] = Field(alias="from", default=None)
    sender_chat: Optional[Chat] = None
    sender_boost_count: Optional[int] = None
    sender_business_bot: Optional[User] = None
    date: int
    business_connection_id: Optional[str] = None
    chat: Chat
    forward_origin: Optional[MessageOrigin] = None
    is_topic_message: Optional[bool] = None
    is_automatic_forward: Optional[bool] = None
    reply_to_message: Optional[Message] = None
    external_reply: Optional[ExternalReplyInfo] = None
    quote: Optional[TextQuote] = None
    reply_to_story: Optional[Union[Story]] = None
    via_bot: Optional[User] = None
    edit_date: Optional[int] = None
    has_protected_content: Optional[bool] = None
    is_from_offline: Optional[bool] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    paid_star_count: Optional[int] = None
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
    effect_id: Optional[str] = None
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    paid_media: Optional[PaidMediaInfo] = None
    photo: Optional[List[PhotoSize]] = None
    sticker: Optional[Sticker] = None
    story: Optional[Union[Story]] = None
    video: Optional[Video] = None
    video_note: Optional[VideoNote] = None
    voice: Optional[Voice] = None
    caption: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    has_media_spoiler: Optional[bool] = None
    contact: Optional[Contact] = None
    dice: Optional[Dice] = None
    game: Optional[Game] = None
    poll: Optional[Poll] = None
    venue: Optional[Venue] = None
    location: Optional[Location] = None
    new_chat_members: Optional[List[User]] = None
    left_chat_member: Optional[User] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Optional[List[PhotoSize]] = None
    delete_chat_photo: Optional[bool] = None
    group_chat_created: Optional[bool] = None
    supergroup_chat_created: Optional[bool] = None
    channel_chat_created: Optional[bool] = None
    message_auto_delete_timer_changed: Optional[MessageAutoDeleteTimerChanged] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    pinned_message: Optional[MaybeInaccessibleMessage] = None
    invoice: Optional[Invoice] = None
    successful_payment: Optional[SuccessfulPayment] = None
    refunded_payment: Optional[RefundedPayment] = None
    users_shared: Optional[UsersShared] = None
    chat_shared: Optional[ChatShared] = None
    gift: Optional[GiftInfo] = None
    unique_gift: Optional[UniqueGiftInfo] = None
    connected_website: Optional[str] = None
    write_access_allowed: Optional[WriteAccessAllowed] = None
    passport_data: Optional[Union[PassportData]] = None
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = None
    boost_added: Optional[ChatBoostAdded] = None
    chat_background_set: Optional[ChatBackground] = None
    forum_topic_created: Optional[Union[ForumTopicCreated]] = None
    forum_topic_edited: Optional[Union[ForumTopicEdited]] = None
    forum_topic_closed: Optional[Union[ForumTopicClosed]] = None
    forum_topic_reopened: Optional[Union[ForumTopicReopened]] = None
    general_forum_topic_hidden: Optional[Union[GeneralForumTopicHidden]] = None
    general_forum_topic_unhidden: Optional[Union[GeneralForumTopicUnhidden]] = None
    giveaway_created: Optional[GiveawayCreated] = None
    giveaway: Optional[Giveaway] = None
    giveaway_winners: Optional[GiveawayWinners] = None
    giveaway_completed: Optional[GiveawayCompleted] = None
    paid_message_price_changed: Optional[PaidMessagePriceChanged] = None
    video_chat_scheduled: Optional[VideoChatScheduled] = None
    video_chat_started: Optional[VideoChatStarted] = None
    video_chat_ended: Optional[VideoChatEnded] = None
    video_chat_participants_invited: Optional[VideoChatParticipantsInvited] = None
    web_app_data: Optional[WebAppData] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
# class: end

# class: start
class MessageId(BaseModel):
    message_id: int
# class: end

# class: start
class InaccessibleMessage(BaseModel):
    chat: Chat
    message_id: int
    date: int
# class: end

# class: start
MaybeInaccessibleMessage = Union[Message, InaccessibleMessage]
# class: end

# class: start
class MessageEntity(BaseModel):
    type: str
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None
    custom_emoji_id: Optional[str] = None
# class: end

# class: start
class TextQuote(BaseModel):
    text: str
    entities: Optional[List[MessageEntity]] = None
    position: int
    is_manual: Optional[bool] = None
# class: end

# class: start
class ExternalReplyInfo(BaseModel):
    origin: MessageOrigin
    chat: Optional[Chat] = None
    message_id: Optional[int] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    paid_media: Optional[PaidMediaInfo] = None
    photo: Optional[List[PhotoSize]] = None
    sticker: Optional[Sticker] = None
    story: Optional[Union[Story]] = None
    video: Optional[Video] = None
    video_note: Optional[VideoNote] = None
    voice: Optional[Voice] = None
    has_media_spoiler: Optional[bool] = None
    contact: Optional[Contact] = None
    dice: Optional[Dice] = None
    game: Optional[Game] = None
    giveaway: Optional[Giveaway] = None
    giveaway_winners: Optional[GiveawayWinners] = None
    invoice: Optional[Invoice] = None
    location: Optional[Location] = None
    poll: Optional[Poll] = None
    venue: Optional[Venue] = None
# class: end

# class: start
class ReplyParameters(BaseModel):
    message_id: int
    chat_id: Optional[Union[int, str]] = None
    allow_sending_without_reply: Optional[bool] = None
    quote: Optional[str] = None
    quote_parse_mode: Optional[str] = None
    quote_entities: Optional[List[MessageEntity]] = None
    quote_position: Optional[int] = None
# class: end

# class: start
MessageOrigin = Union[MessageOriginUser, MessageOriginHiddenUser, MessageOriginChat, MessageOriginChannel]
# class: end

# class: start
class MessageOriginUser(BaseModel):
    type: str
    date: int
    sender_user: User
# class: end

# class: start
class MessageOriginHiddenUser(BaseModel):
    type: str
    date: int
    sender_user_name: str
# class: end

# class: start
class MessageOriginChat(BaseModel):
    type: str
    date: int
    sender_chat: Chat
    author_signature: Optional[str] = None
# class: end

# class: start
class MessageOriginChannel(BaseModel):
    type: str
    date: int
    chat: Chat
    message_id: int
    author_signature: Optional[str] = None
# class: end

# class: start
class PhotoSize(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None
# class: end

# class: start
class Animation(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
# class: end

# class: start
class Audio(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    thumbnail: Optional[PhotoSize] = None
# class: end

# class: start
class Document(BaseModel):
    file_id: str
    file_unique_id: str
    thumbnail: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
# class: end

# class: start
class Story(BaseModel):
    chat: Chat
    id: int
# class: end

# class: start
class Video(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: Optional[PhotoSize] = None
    cover: Optional[List[PhotoSize]] = None
    start_timestamp: Optional[int] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
# class: end

# class: start
class VideoNote(BaseModel):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumbnail: Optional[PhotoSize] = None
    file_size: Optional[int] = None
# class: end

# class: start
class Voice(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
# class: end

# class: start
class PaidMediaInfo(BaseModel):
    star_count: int
    paid_media: List[PaidMedia]
# class: end

# class: start
PaidMedia = Union[PaidMediaPreview, PaidMediaPhoto, PaidMediaVideo]
# class: end

# class: start
class PaidMediaPreview(BaseModel):
    type: str
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
# class: end

# class: start
class PaidMediaPhoto(BaseModel):
    type: str
    photo: List[PhotoSize]
# class: end

# class: start
class PaidMediaVideo(BaseModel):
    type: str
    video: Video
# class: end

# class: start
class Contact(BaseModel):
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[int] = None
    vcard: Optional[str] = None
# class: end

# class: start
class Dice(BaseModel):
    emoji: str
    value: int
# class: end

# class: start
class PollOption(BaseModel):
    text: str
    text_entities: Optional[List[MessageEntity]] = None
    voter_count: int
# class: end

# class: start
class InputPollOption(BaseModel):
    text: str
    text_parse_mode: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None
# class: end

# class: start
class PollAnswer(BaseModel):
    poll_id: str
    voter_chat: Optional[Chat] = None
    user: Optional[User] = None
    option_ids: List[int]
# class: end

# class: start
class Poll(BaseModel):
    id: str
    question: str
    question_entities: Optional[List[MessageEntity]] = None
    options: List[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None
    explanation_entities: Optional[List[MessageEntity]] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None
# class: end

# class: start
class Location(BaseModel):
    latitude: float
    longitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
# class: end

# class: start
class Venue(BaseModel):
    location: Location
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None
# class: end

# class: start
class WebAppData(BaseModel):
    data: str
    button_text: str
# class: end

# class: start
class ProximityAlertTriggered(BaseModel):
    traveler: User
    watcher: User
    distance: int
# class: end

# class: start
class MessageAutoDeleteTimerChanged(BaseModel):
    message_auto_delete_time: int
# class: end

# class: start
class ChatBoostAdded(BaseModel):
    boost_count: int
# class: end

# class: start
BackgroundFill = Union[BackgroundFillSolid, BackgroundFillGradient, BackgroundFillFreeformGradient]
# class: end

# class: start
class BackgroundFillSolid(BaseModel):
    type: str
    color: int
# class: end

# class: start
class BackgroundFillGradient(BaseModel):
    type: str
    top_color: int
    bottom_color: int
    rotation_angle: int
# class: end

# class: start
class BackgroundFillFreeformGradient(BaseModel):
    type: str
    colors: List[int]
# class: end

# class: start
BackgroundType = Union[BackgroundTypeFill, BackgroundTypeWallpaper, BackgroundTypePattern, BackgroundTypeChatTheme]
# class: end

# class: start
class BackgroundTypeFill(BaseModel):
    type: str
    fill: BackgroundFill
    dark_theme_dimming: int
# class: end

# class: start
class BackgroundTypeWallpaper(BaseModel):
    type: str
    document: Document
    dark_theme_dimming: int
    is_blurred: Optional[bool] = None
    is_moving: Optional[bool] = None
# class: end

# class: start
class BackgroundTypePattern(BaseModel):
    type: str
    document: Document
    fill: BackgroundFill
    intensity: int
    is_inverted: Optional[bool] = None
    is_moving: Optional[bool] = None
# class: end

# class: start
class BackgroundTypeChatTheme(BaseModel):
    type: str
    theme_name: str
# class: end

# class: start
class ChatBackground(BaseModel):
    type: BackgroundType
# class: end

# class: start
class ForumTopicCreated(BaseModel):
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None
# class: end

# class: start
from typing import Any
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

class ForumTopicClosed():
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.any_schema()
# class: end

# class: start
class ForumTopicEdited(BaseModel):
    name: Optional[str] = None
    icon_custom_emoji_id: Optional[str] = None
# class: end

# class: start
from typing import Any
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

class ForumTopicReopened():
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.any_schema()
# class: end

# class: start
from typing import Any
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

class GeneralForumTopicHidden():
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.any_schema()
# class: end

# class: start
from typing import Any
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

class GeneralForumTopicUnhidden():
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.any_schema()
# class: end

# class: start
class SharedUser(BaseModel):
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo: Optional[List[PhotoSize]] = None
# class: end

# class: start
class UsersShared(BaseModel):
    request_id: int
    users: List[SharedUser]
# class: end

# class: start
class ChatShared(BaseModel):
    request_id: int
    chat_id: int
    title: Optional[str] = None
    username: Optional[str] = None
    photo: Optional[List[PhotoSize]] = None
# class: end

# class: start
class WriteAccessAllowed(BaseModel):
    from_request: Optional[bool] = None
    web_app_name: Optional[str] = None
    from_attachment_menu: Optional[bool] = None
# class: end

# class: start
class VideoChatScheduled(BaseModel):
    start_date: int
# class: end

# class: start
from typing import Any
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

class VideoChatStarted():
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.any_schema()
# class: end

# class: start
class VideoChatEnded(BaseModel):
    duration: int
# class: end

# class: start
class VideoChatParticipantsInvited(BaseModel):
    users: List[User]
# class: end

# class: start
class PaidMessagePriceChanged(BaseModel):
    paid_message_star_count: int
# class: end

# class: start
class GiveawayCreated(BaseModel):
    prize_star_count: Optional[int] = None
# class: end

# class: start
class Giveaway(BaseModel):
    chats: List[Chat]
    winners_selection_date: int
    winner_count: int
    only_new_members: Optional[bool] = None
    has_public_winners: Optional[bool] = None
    prize_description: Optional[str] = None
    country_codes: Optional[List[str]] = None
    prize_star_count: Optional[int] = None
    premium_subscription_month_count: Optional[int] = None
# class: end

# class: start
class GiveawayWinners(BaseModel):
    chat: Chat
    giveaway_message_id: int
    winners_selection_date: int
    winner_count: int
    winners: List[User]
    additional_chat_count: Optional[int] = None
    prize_star_count: Optional[int] = None
    premium_subscription_month_count: Optional[int] = None
    unclaimed_prize_count: Optional[int] = None
    only_new_members: Optional[bool] = None
    was_refunded: Optional[bool] = None
    prize_description: Optional[str] = None
# class: end

# class: start
class GiveawayCompleted(BaseModel):
    winner_count: int
    unclaimed_prize_count: Optional[int] = None
    giveaway_message: Optional[Message] = None
    is_star_giveaway: Optional[bool] = None
# class: end

# class: start
class LinkPreviewOptions(BaseModel):
    is_disabled: Optional[bool] = None
    url: Optional[str] = None
    prefer_small_media: Optional[bool] = None
    prefer_large_media: Optional[bool] = None
    show_above_text: Optional[bool] = None
# class: end

# class: start
class UserProfilePhotos(BaseModel):
    total_count: int
    photos: List[Array of PhotoSize]
# class: end

# class: start
class File(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None
# class: end

# class: start
class WebAppInfo(BaseModel):
    url: str
# class: end

# class: start
class ReplyKeyboardMarkup(BaseModel):
    keyboard: List[Array of KeyboardButton]
    is_persistent: Optional[bool] = None
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None
# class: end

# class: start
class KeyboardButton(BaseModel):
    text: str
    request_users: Optional[KeyboardButtonRequestUsers] = None
    request_chat: Optional[KeyboardButtonRequestChat] = None
    request_contact: Optional[bool] = None
    request_location: Optional[bool] = None
    request_poll: Optional[KeyboardButtonPollType] = None
    web_app: Optional[WebAppInfo] = None
# class: end

# class: start
class KeyboardButtonRequestUsers(BaseModel):
    request_id: int
    user_is_bot: Optional[bool] = None
    user_is_premium: Optional[bool] = None
    max_quantity: Optional[int] = None
    request_name: Optional[bool] = None
    request_username: Optional[bool] = None
    request_photo: Optional[bool] = None
# class: end

# class: start
class KeyboardButtonRequestChat(BaseModel):
    request_id: int
    chat_is_channel: bool
    chat_is_forum: Optional[bool] = None
    chat_has_username: Optional[bool] = None
    chat_is_created: Optional[bool] = None
    user_administrator_rights: Optional[Union[ChatAdministratorRights]] = None
    bot_administrator_rights: Optional[Union[ChatAdministratorRights]] = None
    bot_is_member: Optional[bool] = None
    request_title: Optional[bool] = None
    request_username: Optional[bool] = None
    request_photo: Optional[bool] = None
# class: end

# class: start
class KeyboardButtonPollType(BaseModel):
    type: Optional[str] = None
# class: end

# class: start
class ReplyKeyboardRemove(BaseModel):
    remove_keyboard: bool
    selective: Optional[bool] = None
# class: end

# class: start
class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: List[Array of InlineKeyboardButton]
# class: end

# class: start
class InlineKeyboardButton(BaseModel):
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None
    web_app: Optional[WebAppInfo] = None
    login_url: Optional[LoginUrl] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    switch_inline_query_chosen_chat: Optional[SwitchInlineQueryChosenChat] = None
    copy_text: Optional[CopyTextButton] = None
    callback_game: Optional[CallbackGame] = None
    pay: Optional[bool] = None
# class: end

# class: start
class LoginUrl(BaseModel):
    url: str
    forward_text: Optional[str] = None
    bot_username: Optional[str] = None
    request_write_access: Optional[bool] = None
# class: end

# class: start
class SwitchInlineQueryChosenChat(BaseModel):
    query: Optional[str] = None
    allow_user_chats: Optional[bool] = None
    allow_bot_chats: Optional[bool] = None
    allow_group_chats: Optional[bool] = None
    allow_channel_chats: Optional[bool] = None
# class: end

# class: start
class CopyTextButton(BaseModel):
    text: str
# class: end

# class: start
class CallbackQuery(BaseModel):
    id: str
    user: User = Field(alias="from")
    message: Optional[MaybeInaccessibleMessage] = None
    inline_message_id: Optional[str] = None
    chat_instance: str
    data: Optional[str] = None
    game_short_name: Optional[str] = None
# class: end

# class: start
class ForceReply(BaseModel):
    force_reply: bool
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None
# class: end

# class: start
class ChatPhoto(BaseModel):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str
# class: end

# class: start
class ChatInviteLink(BaseModel):
    invite_link: str
    creator: User
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: Optional[str] = None
    expire_date: Optional[int] = None
    member_limit: Optional[int] = None
    pending_join_request_count: Optional[int] = None
    subscription_period: Optional[int] = None
    subscription_price: Optional[int] = None
# class: end

# class: start
class ChatAdministratorRights(BaseModel):
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_stories: bool
    can_edit_stories: bool
    can_delete_stories: bool
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
# class: end

# class: start
class ChatMemberUpdated(BaseModel):
    chat: Chat
    user: User = Field(alias="from")
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink] = None
    via_join_request: Optional[bool] = None
    via_chat_folder_invite_link: Optional[bool] = None
# class: end

# class: start
ChatMember = Union[ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMemberRestricted, ChatMemberLeft, ChatMemberBanned]
# class: end

# class: start
class ChatMemberOwner(BaseModel):
    status: str
    user: User
    is_anonymous: bool
    custom_title: Optional[str] = None
# class: end

# class: start
class ChatMemberAdministrator(BaseModel):
    status: str
    user: User
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_stories: bool
    can_edit_stories: bool
    can_delete_stories: bool
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
    custom_title: Optional[str] = None
# class: end

# class: start
class ChatMemberMember(BaseModel):
    status: str
    user: User
    until_date: Optional[int] = None
# class: end

# class: start
class ChatMemberRestricted(BaseModel):
    status: str
    user: User
    is_member: bool
    can_send_messages: bool
    can_send_audios: bool
    can_send_documents: bool
    can_send_photos: bool
    can_send_videos: bool
    can_send_video_notes: bool
    can_send_voice_notes: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_manage_topics: bool
    until_date: int
# class: end

# class: start
class ChatMemberLeft(BaseModel):
    status: str
    user: User
# class: end

# class: start
class ChatMemberBanned(BaseModel):
    status: str
    user: User
    until_date: int
# class: end

# class: start
class ChatJoinRequest(BaseModel):
    chat: Chat
    user: User = Field(alias="from")
    user_chat_id: int
    date: int
    bio: Optional[str] = None
    invite_link: Optional[ChatInviteLink] = None
# class: end

# class: start
class ChatPermissions(BaseModel):
    can_send_messages: Optional[bool] = None
    can_send_audios: Optional[bool] = None
    can_send_documents: Optional[bool] = None
    can_send_photos: Optional[bool] = None
    can_send_videos: Optional[bool] = None
    can_send_video_notes: Optional[bool] = None
    can_send_voice_notes: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
# class: end

# class: start
class Birthdate(BaseModel):
    day: int
    month: int
    year: Optional[int] = None
# class: end

# class: start
class BusinessIntro(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    sticker: Optional[Sticker] = None
# class: end

# class: start
class BusinessLocation(BaseModel):
    address: str
    location: Optional[Location] = None
# class: end

# class: start
class BusinessOpeningHoursInterval(BaseModel):
    opening_minute: int
    closing_minute: int
# class: end

# class: start
class BusinessOpeningHours(BaseModel):
    time_zone_name: str
    opening_hours: List[BusinessOpeningHoursInterval]
# class: end

# class: start
class StoryAreaPosition(BaseModel):
    x_percentage: float
    y_percentage: float
    width_percentage: float
    height_percentage: float
    rotation_angle: float
    corner_radius_percentage: float
# class: end

# class: start
class LocationAddress(BaseModel):
    country_code: str
    state: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
# class: end

# class: start
StoryAreaType = Union[StoryAreaTypeLocation, StoryAreaTypeSuggestedReaction, StoryAreaTypeLink, StoryAreaTypeWeather, StoryAreaTypeUniqueGift]
# class: end

# class: start
class StoryAreaTypeLocation(BaseModel):
    type: str
    latitude: float
    longitude: float
    address: Optional[LocationAddress] = None
# class: end

# class: start
class StoryAreaTypeSuggestedReaction(BaseModel):
    type: str
    reaction_type: ReactionType
    is_dark: Optional[bool] = None
    is_flipped: Optional[bool] = None
# class: end

# class: start
class StoryAreaTypeLink(BaseModel):
    type: str
    url: str
# class: end

# class: start
class StoryAreaTypeWeather(BaseModel):
    type: str
    temperature: float
    emoji: str
    background_color: int
# class: end

# class: start
class StoryAreaTypeUniqueGift(BaseModel):
    type: str
    name: str
# class: end

# class: start
class StoryArea(BaseModel):
    position: Union[StoryAreaPosition]
    type: Union[StoryAreaType]
# class: end

# class: start
class ChatLocation(BaseModel):
    location: Location
    address: str
# class: end

# class: start
ReactionType = Union[ReactionTypeEmoji, ReactionTypeCustomEmoji, ReactionTypePaid]
# class: end

# class: start
class ReactionTypeEmoji(BaseModel):
    type: str
    emoji: str
# class: end

# class: start
class ReactionTypeCustomEmoji(BaseModel):
    type: str
    custom_emoji_id: str
# class: end

# class: start
class ReactionTypePaid(BaseModel):
    type: str
# class: end

# class: start
class ReactionCount(BaseModel):
    type: ReactionType
    total_count: int
# class: end

# class: start
class MessageReactionUpdated(BaseModel):
    chat: Chat
    message_id: int
    user: Optional[User] = None
    actor_chat: Optional[Chat] = None
    date: int
    old_reaction: List[ReactionType]
    new_reaction: List[ReactionType]
# class: end

# class: start
class MessageReactionCountUpdated(BaseModel):
    chat: Chat
    message_id: int
    date: int
    reactions: List[ReactionCount]
# class: end

# class: start
class ForumTopic(BaseModel):
    message_thread_id: int
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None
# class: end

# class: start
class Gift(BaseModel):
    id: str
    sticker: Sticker
    star_count: int
    upgrade_star_count: Optional[int] = None
    total_count: Optional[int] = None
    remaining_count: Optional[int] = None
# class: end

# class: start
class Gifts(BaseModel):
    gifts: List[Gift]
# class: end

# class: start
class UniqueGiftModel(BaseModel):
    name: str
    sticker: Sticker
    rarity_per_mille: int
# class: end

# class: start
class UniqueGiftSymbol(BaseModel):
    name: str
    sticker: Sticker
    rarity_per_mille: int
# class: end

# class: start
class UniqueGiftBackdropColors(BaseModel):
    center_color: int
    edge_color: int
    symbol_color: int
    text_color: int
# class: end

# class: start
class UniqueGiftBackdrop(BaseModel):
    name: str
    colors: Union[UniqueGiftBackdropColors]
    rarity_per_mille: int
# class: end

# class: start
class UniqueGift(BaseModel):
    base_name: str
    name: str
    number: int
    model: UniqueGiftModel
    symbol: UniqueGiftSymbol
    backdrop: UniqueGiftBackdrop
# class: end

# class: start
class GiftInfo(BaseModel):
    gift: Gift
    owned_gift_id: Optional[str] = None
    convert_star_count: Optional[int] = None
    prepaid_upgrade_star_count: Optional[int] = None
    can_be_upgraded: Optional[bool] = None
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    is_private: Optional[bool] = None
# class: end

# class: start
class UniqueGiftInfo(BaseModel):
    gift: UniqueGift
    origin: str
    owned_gift_id: Optional[str] = None
    transfer_star_count: Optional[int] = None
# class: end

# class: start
OwnedGift = Union[OwnedGiftRegular, OwnedGiftUnique]
# class: end

# class: start
class OwnedGiftRegular(BaseModel):
    type: str
    gift: Gift
    owned_gift_id: Optional[str] = None
    sender_user: Optional[User] = None
    send_date: int
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    is_private: Optional[bool] = None
    is_saved: Optional[bool] = None
    can_be_upgraded: Optional[bool] = None
    was_refunded: Optional[bool] = None
    convert_star_count: Optional[int] = None
    prepaid_upgrade_star_count: Optional[int] = None
# class: end

# class: start
class OwnedGiftUnique(BaseModel):
    type: str
    gift: UniqueGift
    owned_gift_id: Optional[str] = None
    sender_user: Optional[User] = None
    send_date: int
    is_saved: Optional[bool] = None
    can_be_transferred: Optional[bool] = None
    transfer_star_count: Optional[int] = None
# class: end

# class: start
class OwnedGifts(BaseModel):
    total_count: int
    gifts: List[OwnedGift]
    next_offset: Optional[str] = None
# class: end

# class: start
class AcceptedGiftTypes(BaseModel):
    unlimited_gifts: bool
    limited_gifts: bool
    unique_gifts: bool
    premium_subscription: bool
# class: end

# class: start
class StarAmount(BaseModel):
    amount: int
    nanostar_amount: Optional[int] = None
# class: end

# class: start
class BotCommand(BaseModel):
    command: str
    description: str
# class: end

# class: start
BotCommandScope = Union[BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, BotCommandScopeAllChatAdministrators, BotCommandScopeChat, BotCommandScopeChatAdministrators, BotCommandScopeChatMember]
# class: end

# class: start
class BotCommandScopeDefault(BaseModel):
    type: str
# class: end

# class: start
class BotCommandScopeAllPrivateChats(BaseModel):
    type: str
# class: end

# class: start
class BotCommandScopeAllGroupChats(BaseModel):
    type: str
# class: end

# class: start
class BotCommandScopeAllChatAdministrators(BaseModel):
    type: str
# class: end

# class: start
class BotCommandScopeChat(BaseModel):
    type: str
    chat_id: Union[int, str]
# class: end

# class: start
class BotCommandScopeChatAdministrators(BaseModel):
    type: str
    chat_id: Union[int, str]
# class: end

# class: start
class BotCommandScopeChatMember(BaseModel):
    type: str
    chat_id: Union[int, str]
    user_id: int
# class: end

# class: start
class BotName(BaseModel):
    name: str
# class: end

# class: start
class BotDescription(BaseModel):
    description: str
# class: end

# class: start
class BotShortDescription(BaseModel):
    short_description: str
# class: end

# class: start
MenuButton = Union[MenuButtonCommands, MenuButtonWebApp, MenuButtonDefault]
# class: end

# class: start
class MenuButtonCommands(BaseModel):
    type: str
# class: end

# class: start
class MenuButtonWebApp(BaseModel):
    type: str
    text: str
    web_app: WebAppInfo
# class: end

# class: start
class MenuButtonDefault(BaseModel):
    type: str
# class: end

# class: start
ChatBoostSource = Union[ChatBoostSourcePremium, ChatBoostSourceGiftCode, ChatBoostSourceGiveaway]
# class: end

# class: start
class ChatBoostSourcePremium(BaseModel):
    source: str
    user: User
# class: end

# class: start
class ChatBoostSourceGiftCode(BaseModel):
    source: str
    user: User
# class: end

# class: start
class ChatBoostSourceGiveaway(BaseModel):
    source: str
    giveaway_message_id: int
    user: Optional[User] = None
    prize_star_count: Optional[int] = None
    is_unclaimed: Optional[bool] = None
# class: end

# class: start
class ChatBoost(BaseModel):
    boost_id: str
    add_date: int
    expiration_date: int
    source: ChatBoostSource
# class: end

# class: start
class ChatBoostUpdated(BaseModel):
    chat: Chat
    boost: ChatBoost
# class: end

# class: start
class ChatBoostRemoved(BaseModel):
    chat: Chat
    boost_id: str
    remove_date: int
    source: ChatBoostSource
# class: end

# class: start
class UserChatBoosts(BaseModel):
    boosts: List[ChatBoost]
# class: end

# class: start
class BusinessBotRights(BaseModel):
    can_reply: Optional[bool] = None
    can_read_messages: Optional[bool] = None
    can_delete_sent_messages: Optional[bool] = None
    can_delete_all_messages: Optional[bool] = None
    can_edit_name: Optional[bool] = None
    can_edit_bio: Optional[bool] = None
    can_edit_profile_photo: Optional[bool] = None
    can_edit_username: Optional[bool] = None
    can_change_gift_settings: Optional[bool] = None
    can_view_gifts_and_stars: Optional[bool] = None
    can_convert_gifts_to_stars: Optional[bool] = None
    can_transfer_and_upgrade_gifts: Optional[bool] = None
    can_transfer_stars: Optional[bool] = None
    can_manage_stories: Optional[bool] = None
# class: end

# class: start
class BusinessConnection(BaseModel):
    id: str
    user: User
    user_chat_id: int
    date: int
    rights: Optional[BusinessBotRights] = None
    is_enabled: bool
# class: end

# class: start
class BusinessMessagesDeleted(BaseModel):
    business_connection_id: str
    chat: Chat
    message_ids: List[int]
# class: end

# class: start
class ResponseParameters(BaseModel):
    migrate_to_chat_id: Optional[int] = None
    retry_after: Optional[int] = None
# class: end

# class: start
InputMedia = Union[InputMediaAnimation, InputMediaDocument, InputMediaAudio, InputMediaPhoto, InputMediaVideo]
# class: end

# class: start
class InputMediaPhoto(BaseModel):
    type: str
    media: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    has_spoiler: Optional[bool] = None
# class: end

# class: start
class InputMediaVideo(BaseModel):
    type: str
    media: str
    thumbnail: Optional[str] = None
    cover: Optional[str] = None
    start_timestamp: Optional[int] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    supports_streaming: Optional[bool] = None
    has_spoiler: Optional[bool] = None
# class: end

# class: start
class InputMediaAnimation(BaseModel):
    type: str
    media: str
    thumbnail: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    has_spoiler: Optional[bool] = None
# class: end

# class: start
class InputMediaAudio(BaseModel):
    type: str
    media: str
    thumbnail: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    duration: Optional[int] = None
    performer: Optional[str] = None
    title: Optional[str] = None
# class: end

# class: start
class InputMediaDocument(BaseModel):
    type: str
    media: str
    thumbnail: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    disable_content_type_detection: Optional[bool] = None
# class: end

# class: start
from typing import Any
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

class InputFile():
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.any_schema()
# class: end

# class: start
InputPaidMedia = Union[InputPaidMediaPhoto, InputPaidMediaVideo]
# class: end

# class: start
class InputPaidMediaPhoto(BaseModel):
    type: str
    media: str
# class: end

# class: start
class InputPaidMediaVideo(BaseModel):
    type: str
    media: str
    thumbnail: Optional[str] = None
    cover: Optional[str] = None
    start_timestamp: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    supports_streaming: Optional[bool] = None
# class: end

# class: start
InputProfilePhoto = Union[InputProfilePhotoStatic, InputProfilePhotoAnimated]
# class: end

# class: start
class InputProfilePhotoStatic(BaseModel):
    type: str
    photo: str
# class: end

# class: start
class InputProfilePhotoAnimated(BaseModel):
    type: str
    animation: str
    main_frame_timestamp: Optional[float] = None
# class: end

# class: start
InputStoryContent = Union[InputStoryContentPhoto, InputStoryContentVideo]
# class: end

# class: start
class InputStoryContentPhoto(BaseModel):
    type: str
    photo: str
# class: end

# class: start
class InputStoryContentVideo(BaseModel):
    type: str
    video: str
    duration: Optional[float] = None
    cover_frame_timestamp: Optional[float] = None
    is_animation: Optional[bool] = None
# class: end