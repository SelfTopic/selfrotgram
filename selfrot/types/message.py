from typing import Optional, Self, Any
from .user import User
from .chat import Chat
from pydantic import BaseModel, Field


class Message(BaseModel):
    
    user: Optional[User] = Field(alias="from")
    reply_message: Optional[Self] = None
    chat: Chat 
    text: Optional[str]
    message_id: int
    date: int 
    entities: list[dict[str, Any]]
