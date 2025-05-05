from typing import List, Optional
from pydantic import BaseModel
from .message_entity import MessageEntity

class InputMediaPhoto(BaseModel):
    type: str
    media: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    has_spoiler: Optional[bool] = None