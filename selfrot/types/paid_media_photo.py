from typing import List
from pydantic import BaseModel
from .photo_size import PhotoSize

class PaidMediaPhoto(BaseModel):
    type: str
    photo: List[PhotoSize]