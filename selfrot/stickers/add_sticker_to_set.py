from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from .input_sticker import InputSticker

@dataclass
class AddStickerToSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "addStickerToSet"
    user_id: int
    name: str
    sticker: InputSticker