from typing import Optional
from pydantic import BaseModel
from .user import User
from .business_bot_rights import BusinessBotRights

class BusinessConnection(BaseModel):
    id: str
    user: User
    user_chat_id: int
    date: int
    rights: Optional[BusinessBotRights] = None
    is_enabled: bool