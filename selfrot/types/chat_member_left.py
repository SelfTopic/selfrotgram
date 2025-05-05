from pydantic import BaseModel
from .user import User

class ChatMemberLeft(BaseModel):
    status: str
    user: User