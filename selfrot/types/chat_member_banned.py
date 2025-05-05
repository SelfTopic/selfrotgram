from pydantic import BaseModel
from .user import User

class ChatMemberBanned(BaseModel):
    status: str
    user: User
    until_date: int