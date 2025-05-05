from pydantic import BaseModel
from .user import User

class MessageOriginUser(BaseModel):
    type: str
    date: int
    sender_user: User