from typing import List, Optional
from pydantic import BaseModel
from .photo_size import PhotoSize

class ChatShared(BaseModel):
    request_id: int
    chat_id: int
    title: Optional[str] = None
    username: Optional[str] = None
    photo: Optional[List[PhotoSize]] = None