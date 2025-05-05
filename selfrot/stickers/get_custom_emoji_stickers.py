from typing import List, ClassVar
from ..methods.base import TelegramAPIMethod
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class GetCustomEmojiStickers(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getCustomEmojiStickers"
    custom_emoji_ids: List[str]