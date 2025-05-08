from typing import List, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetStickerEmojiList(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerEmojiList"
    sticker: str
    emoji_list: List[str]