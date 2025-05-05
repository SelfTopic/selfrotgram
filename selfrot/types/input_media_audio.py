from typing import List, Optional
from pydantic import BaseModel
from .message_entity import MessageEntity

class InputMediaAudio(BaseModel):
    type: str
    media: str
    thumbnail: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    duration: Optional[int] = None
    performer: Optional[str] = None
    title: Optional[str] = None