from typing import Optional
from pydantic import BaseModel
from .chat import Chat

class MessageOriginChannel(BaseModel):
    type: str
    date: int
    chat: Chat
    message_id: int
    author_signature: Optional[str] = None