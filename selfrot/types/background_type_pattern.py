from typing import Optional
from pydantic import BaseModel
from .background_fill import BackgroundFill
from .document import Document

class BackgroundTypePattern(BaseModel):
    type: str
    document: Document
    fill: BackgroundFill
    intensity: int
    is_inverted: Optional[bool] = None
    is_moving: Optional[bool] = None