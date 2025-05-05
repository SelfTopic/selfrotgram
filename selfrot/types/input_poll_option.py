from typing import List, Optional
from pydantic import BaseModel
from .message_entity import MessageEntity

class InputPollOption(BaseModel):
    text: str
    text_parse_mode: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None