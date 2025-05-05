from typing import List, Optional
from pydantic import BaseModel
from .photo_size import PhotoSize

class SharedUser(BaseModel):
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo: Optional[List[PhotoSize]] = None