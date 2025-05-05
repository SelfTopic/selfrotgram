from typing import List, Optional
from pydantic import BaseModel
from .message_entity import MessageEntity

class InputMediaAnimation(BaseModel):
    type: str
    media: str
    thumbnail: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    has_spoiler: Optional[bool] = None