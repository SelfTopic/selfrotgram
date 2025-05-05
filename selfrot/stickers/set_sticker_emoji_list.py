from typing import List, ClassVar
from ..methods.base import TelegramAPIMethod
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class SetStickerEmojiList(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerEmojiList"
    sticker: str
    emoji_list: List[str]