from typing import Optional
from pydantic import BaseModel
from .document import Document
from .background_fill import BackgroundFill

class BackgroundTypePattern(BaseModel):
    type: str
    document: Document
    fill: BackgroundFill
    intensity: int
    is_inverted: Optional[bool] = None
    is_moving: Optional[bool] = None