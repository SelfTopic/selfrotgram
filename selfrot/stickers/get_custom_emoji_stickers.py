from typing import List, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetCustomEmojiStickers(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getCustomEmojiStickers"
    custom_emoji_ids: List[str]