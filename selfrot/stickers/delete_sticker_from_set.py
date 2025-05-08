from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class DeleteStickerFromSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteStickerFromSet"
    sticker: str