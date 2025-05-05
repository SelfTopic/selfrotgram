from typing import Optional, Union, List, ClassVar
from pydantic import BaseModel
from dataclasses import dataclass

# class: start
class Sticker(BaseModel):
    file_id: str
    file_unique_id: str
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumbnail: Optional[PhotoSize] = None
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    premium_animation: Optional[File] = None
    mask_position: Optional[MaskPosition] = None
    custom_emoji_id: Optional[str] = None
    needs_repainting: Optional[bool] = None
    file_size: Optional[int] = None
# class: end

# class: start
class StickerSet(BaseModel):
    name: str
    title: str
    sticker_type: str
    stickers: List[Sticker]
    thumbnail: Optional[PhotoSize] = None
# class: end

# class: start
class MaskPosition(BaseModel):
    point: str
    x_shift: float
    y_shift: float
    scale: float
# class: end

# class: start
class InputSticker(BaseModel):
    sticker: str
    format: str
    emoji_list: List[str]
    mask_position: Optional[MaskPosition] = None
    keywords: Optional[List[str]] = None
# class: end

# class: start
@dataclass
class SendSticker(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendSticker"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    sticker: Union[InputFile, str]
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
class GetStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getStickerSet"
    name: str
# class: end

# class: start
@dataclass
class GetCustomEmojiStickers(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getCustomEmojiStickers"
    custom_emoji_ids: List[str]
# class: end

# class: start
@dataclass
class UploadStickerFile(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "uploadStickerFile"
    user_id: int
    sticker: InputFile
    sticker_format: str
# class: end

# class: start
@dataclass
class CreateNewStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "createNewStickerSet"
    user_id: int
    name: str
    title: str
    stickers: List[InputSticker]
    sticker_type: Optional[str] = None
    needs_repainting: Optional[bool] = None
# class: end

# class: start
@dataclass
class AddStickerToSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "addStickerToSet"
    user_id: int
    name: str
    sticker: InputSticker
# class: end

# class: start
@dataclass
class SetStickerPositionInSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerPositionInSet"
    sticker: str
    position: int
# class: end

# class: start
@dataclass
class DeleteStickerFromSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteStickerFromSet"
    sticker: str
# class: end

# class: start
@dataclass
class ReplaceStickerInSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "replaceStickerInSet"
    user_id: int
    name: str
    old_sticker: str
    sticker: InputSticker
# class: end

# class: start
@dataclass
class SetStickerEmojiList(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerEmojiList"
    sticker: str
    emoji_list: List[str]
# class: end

# class: start
@dataclass
class SetStickerKeywords(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerKeywords"
    sticker: str
    keywords: Optional[List[str]] = None
# class: end

# class: start
@dataclass
class SetStickerMaskPosition(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerMaskPosition"
    sticker: str
    mask_position: Optional[MaskPosition] = None
# class: end

# class: start
@dataclass
class SetStickerSetTitle(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerSetTitle"
    name: str
    title: str
# class: end

# class: start
@dataclass
class SetStickerSetThumbnail(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerSetThumbnail"
    name: str
    user_id: int
    thumbnail: Optional[Union[InputFile, str]] = None
    format: str
# class: end

# class: start
@dataclass
class SetCustomEmojiStickerSetThumbnail(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setCustomEmojiStickerSetThumbnail"
    name: str
    custom_emoji_id: Optional[str] = None
# class: end

# class: start
@dataclass
class DeleteStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteStickerSet"
    name: str
# class: end
