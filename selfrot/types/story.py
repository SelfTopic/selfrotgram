from pydantic import BaseModel
from .chat import Chat

class Story(BaseModel):
    chat: Chat
    id: int