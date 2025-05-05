from typing import Optional, ClassVar
from ..methods.base import TelegramAPIMethod
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class SetCustomEmojiStickerSetThumbnail(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setCustomEmojiStickerSetThumbnail"
    name: str
    custom_emoji_id: Optional[str] = None