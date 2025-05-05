from typing import Optional
from pydantic import BaseModel
from .user import User

class ChatMemberMember(BaseModel):
    status: str
    user: User
    until_date: Optional[int] = None