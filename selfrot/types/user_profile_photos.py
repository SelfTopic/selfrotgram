from typing import List
from pydantic import BaseModel
from .array of _photo_size import Array of PhotoSize

class UserProfilePhotos(BaseModel):
    total_count: int
    photos: List[Array of PhotoSize]