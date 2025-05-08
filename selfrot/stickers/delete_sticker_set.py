from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class DeleteStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteStickerSet"
    name: str