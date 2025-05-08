from pydantic import BaseModel
from .chat import Chat

class InaccessibleMessage(BaseModel):
    chat: Chat
    message_id: int
    date: int