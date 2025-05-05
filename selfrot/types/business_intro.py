from typing import Optional
from pydantic import BaseModel
from ..stickers.sticker import Sticker

class BusinessIntro(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    sticker: Optional[Sticker] = None