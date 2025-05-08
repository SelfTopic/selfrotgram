from typing import Optional
from pydantic import BaseModel
from .business_bot_rights import BusinessBotRights
from .user import User

class BusinessConnection(BaseModel):
    id: str
    user: User
    user_chat_id: int
    date: int
    rights: Optional[BusinessBotRights] = None
    is_enabled: bool