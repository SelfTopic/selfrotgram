from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetStickerSetTitle(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerSetTitle"
    name: str
    title: str