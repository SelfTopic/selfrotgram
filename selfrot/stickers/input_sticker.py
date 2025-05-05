from typing import List, Optional
from pydantic import BaseModel
from .mask_position import MaskPosition

class InputSticker(BaseModel):
    sticker: str
    format: str
    emoji_list: List[str]
    mask_position: Optional[MaskPosition] = None
    keywords: Optional[List[str]] = None