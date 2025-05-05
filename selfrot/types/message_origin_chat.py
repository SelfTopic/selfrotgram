from typing import Optional
from pydantic import BaseModel
from .chat import Chat

class MessageOriginChat(BaseModel):
    type: str
    date: int
    sender_chat: Chat
    author_signature: Optional[str] = None