from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetStickerPositionInSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerPositionInSet"
    sticker: str
    position: int