from typing import Optional
from pydantic import BaseModel
from .document import Document

class BackgroundTypeWallpaper(BaseModel):
    type: str
    document: Document
    dark_theme_dimming: int
    is_blurred: Optional[bool] = None
    is_moving: Optional[bool] = None