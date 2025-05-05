from typing import List, Optional
from pydantic import BaseModel
from .photo_size import PhotoSize

class Video(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: Optional[PhotoSize] = None
    cover: Optional[List[PhotoSize]] = None
    start_timestamp: Optional[int] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None