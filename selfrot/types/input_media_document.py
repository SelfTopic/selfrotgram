from typing import List, Optional
from pydantic import BaseModel
from .message_entity import MessageEntity

class InputMediaDocument(BaseModel):
    type: str
    media: str
    thumbnail: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    disable_content_type_detection: Optional[bool] = None