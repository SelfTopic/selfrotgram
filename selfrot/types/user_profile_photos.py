from typing import List
from pydantic import BaseModel
from .photo_size import PhotoSize

class UserProfilePhotos(BaseModel):
    total_count: int
    photos: List[List[PhotoSize]]