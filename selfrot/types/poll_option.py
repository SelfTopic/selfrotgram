from typing import List, Optional
from pydantic import BaseModel
from .message_entity import MessageEntity

class PollOption(BaseModel):
    text: str
    text_entities: Optional[List[MessageEntity]] = None
    voter_count: int