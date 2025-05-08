from typing import List, Optional
from pydantic import BaseModel
from ..types import PhotoSize
from .sticker import Sticker

class StickerSet(BaseModel):
    name: str
    title: str
    sticker_type: str
    stickers: List[Sticker]
    thumbnail: Optional[PhotoSize] = None