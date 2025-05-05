from typing import List
from pydantic import BaseModel
from .chat import Chat

class BusinessMessagesDeleted(BaseModel):
    business_connection_id: str
    chat: Chat
    message_ids: List[int]