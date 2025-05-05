from typing import List, Optional
from pydantic import BaseModel
from .message_entity import MessageEntity

class InputMediaVideo(BaseModel):
    type: str
    media: str
    thumbnail: Optional[str] = None
    cover: Optional[str] = None
    start_timestamp: Optional[int] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    supports_streaming: Optional[bool] = None
    has_spoiler: Optional[bool] = None