from typing import Optional, ClassVar
from ..methods.base import TelegramAPIMethod
from pydantic import BaseModel
from dataclasses import dataclass
from .mask_position import MaskPosition

@dataclass
class SetStickerMaskPosition(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerMaskPosition"
    sticker: str
    mask_position: Optional[MaskPosition] = None