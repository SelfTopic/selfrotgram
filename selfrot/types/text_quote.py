from typing import List, Optional
from pydantic import BaseModel
from .message_entity import MessageEntity

class TextQuote(BaseModel):
    text: str
    entities: Optional[List[MessageEntity]] = None
    position: int
    is_manual: Optional[bool] = None