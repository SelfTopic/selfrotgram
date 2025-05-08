from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from .input_sticker import InputSticker

@dataclass
class ReplaceStickerInSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "replaceStickerInSet"
    user_id: int
    name: str
    old_sticker: str
    sticker: InputSticker