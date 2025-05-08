from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getStickerSet"
    name: str