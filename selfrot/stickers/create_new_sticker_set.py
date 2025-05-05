from typing import List, Optional, ClassVar
from ..methods.base import TelegramAPIMethod
from pydantic import BaseModel
from dataclasses import dataclass
from .input_sticker import InputSticker

@dataclass
class CreateNewStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "createNewStickerSet"
    user_id: int
    name: str
    title: str
    stickers: List[InputSticker]
    sticker_type: Optional[str] = None
    needs_repainting: Optional[bool] = None