from typing import Optional
from pydantic import BaseModel
from .user import User

class ChatMemberOwner(BaseModel):
    status: str
    user: User
    is_anonymous: bool
    custom_title: Optional[str] = None