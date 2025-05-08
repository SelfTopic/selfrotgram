
# class: start
@dataclass
class EditMessageText(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editMessageText"
    business_connection_id: Optional[str] = None
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    text: str
    parse_mode: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
# class: end

# class: start
@dataclass
class EditMessageCaption(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editMessageCaption"
    business_connection_id: Optional[str] = None
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
# class: end

# class: start
@dataclass
class EditMessageMedia(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editMessageMedia"
    business_connection_id: Optional[str] = None
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    media: InputMedia
    reply_markup: Optional[InlineKeyboardMarkup] = None
# class: end

# class: start
@dataclass
class EditMessageLiveLocation(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editMessageLiveLocation"
    business_connection_id: Optional[str] = None
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    latitude: float
    longitude: float
    live_period: Optional[int] = None
    horizontal_accuracy: Optional[float] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
# class: end

# class: start
@dataclass
class StopMessageLiveLocation(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "stopMessageLiveLocation"
    business_connection_id: Optional[str] = None
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
# class: end

# class: start
@dataclass
class EditMessageReplyMarkup(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editMessageReplyMarkup"
    business_connection_id: Optional[str] = None
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
# class: end

# class: start
@dataclass
class StopPoll(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "stopPoll"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_id: int
    reply_markup: Optional[InlineKeyboardMarkup] = None
# class: end

# class: start
@dataclass
class DeleteMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteMessage"
    chat_id: Union[int, str]
    message_id: int
# class: end

# class: start
@dataclass
class DeleteMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteMessages"
    chat_id: Union[int, str]
    message_ids: List[int]
# class: end

# class: start
from typing import ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetAvailableGifts(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getAvailableGifts"
# class: end

# class: start
@dataclass
class SendGift(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendGift"
    user_id: Optional[int] = None
    chat_id: Optional[Union[int, str]] = None
    gift_id: str
    pay_for_upgrade: Optional[bool] = None
    text: Optional[str] = None
    text_parse_mode: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None
# class: end

# class: start
@dataclass
class GiftPremiumSubscription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "giftPremiumSubscription"
    user_id: int
    month_count: int
    star_count: int
    text: Optional[str] = None
    text_parse_mode: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None
# class: end

# class: start
@dataclass
class VerifyUser(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "verifyUser"
    user_id: int
    custom_description: Optional[str] = None
# class: end

# class: start
@dataclass
class VerifyChat(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "verifyChat"
    chat_id: Union[int, str]
    custom_description: Optional[str] = None
# class: end

# class: start
@dataclass
class RemoveUserVerification(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "removeUserVerification"
    user_id: int
# class: end

# class: start
@dataclass
class RemoveChatVerification(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "removeChatVerification"
    chat_id: Union[int, str]
# class: end

# class: start
@dataclass
class ReadBusinessMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "readBusinessMessage"
    business_connection_id: str
    chat_id: int
    message_id: int
# class: end

# class: start
@dataclass
class DeleteBusinessMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteBusinessMessages"
    business_connection_id: str
    message_ids: List[int]
# class: end

# class: start
@dataclass
class SetBusinessAccountName(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setBusinessAccountName"
    business_connection_id: str
    first_name: str
    last_name: Optional[str] = None
# class: end

# class: start
@dataclass
class SetBusinessAccountUsername(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setBusinessAccountUsername"
    business_connection_id: str
    username: Optional[str] = None
# class: end

# class: start
@dataclass
class SetBusinessAccountBio(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setBusinessAccountBio"
    business_connection_id: str
    bio: Optional[str] = None
# class: end

# class: start
@dataclass
class SetBusinessAccountProfilePhoto(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setBusinessAccountProfilePhoto"
    business_connection_id: str
    photo: InputProfilePhoto
    is_public: Optional[bool] = None
# class: end

# class: start
@dataclass
class RemoveBusinessAccountProfilePhoto(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "removeBusinessAccountProfilePhoto"
    business_connection_id: str
    is_public: Optional[bool] = None
# class: end

# class: start
@dataclass
class SetBusinessAccountGiftSettings(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setBusinessAccountGiftSettings"
    business_connection_id: str
    show_gift_button: bool
    accepted_gift_types: AcceptedGiftTypes
# class: end

# class: start
@dataclass
class GetBusinessAccountStarBalance(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getBusinessAccountStarBalance"
    business_connection_id: str
# class: end

# class: start
@dataclass
class TransferBusinessAccountStars(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "transferBusinessAccountStars"
    business_connection_id: str
    star_count: int
# class: end

# class: start
@dataclass
class GetBusinessAccountGifts(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getBusinessAccountGifts"
    business_connection_id: str
    exclude_unsaved: Optional[bool] = None
    exclude_saved: Optional[bool] = None
    exclude_unlimited: Optional[bool] = None
    exclude_limited: Optional[bool] = None
    exclude_unique: Optional[bool] = None
    sort_by_price: Optional[bool] = None
    offset: Optional[str] = None
    limit: Optional[int] = None
# class: end

# class: start
@dataclass
class ConvertGiftToStars(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "convertGiftToStars"
    business_connection_id: str
    owned_gift_id: str
# class: end

# class: start
@dataclass
class UpgradeGift(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "upgradeGift"
    business_connection_id: str
    owned_gift_id: str
    keep_original_details: Optional[bool] = None
    star_count: Optional[int] = None
# class: end

# class: start
@dataclass
class TransferGift(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "transferGift"
    business_connection_id: str
    owned_gift_id: str
    new_owner_chat_id: int
    star_count: Optional[int] = None
# class: end

# class: start
@dataclass
class PostStory(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "postStory"
    business_connection_id: str
    content: Union[InputStoryContent]
    active_period: int
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    areas: Optional[Union[List[StoryArea]]] = None
    post_to_chat_page: Optional[bool] = None
    protect_content: Optional[bool] = None
# class: end

# class: start
@dataclass
class EditStory(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editStory"
    business_connection_id: str
    story_id: int
    content: Union[InputStoryContent]
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    areas: Optional[Union[List[StoryArea]]] = None
# class: end

# class: start
@dataclass
class DeleteStory(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteStory"
    business_connection_id: str
    story_id: int
# class: end
