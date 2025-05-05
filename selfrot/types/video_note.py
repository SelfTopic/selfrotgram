from typing import Optional
from pydantic import BaseModel
from .photo_size import PhotoSize

class VideoNote(BaseModel):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumbnail: Optional[PhotoSize] = None
    file_size: Optional[int] = None