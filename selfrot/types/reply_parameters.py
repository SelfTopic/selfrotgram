from typing import Union, List, Optional
from pydantic import BaseModel
from .message_entity import MessageEntity

class ReplyParameters(BaseModel):
    message_id: int
    chat_id: Optional[Union[int, str]] = None
    allow_sending_without_reply: Optional[bool] = None
    quote: Optional[str] = None
    quote_parse_mode: Optional[str] = None
    quote_entities: Optional[List[MessageEntity]] = None
    quote_position: Optional[int] = None