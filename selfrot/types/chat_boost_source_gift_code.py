from pydantic import BaseModel
from .user import User

class ChatBoostSourceGiftCode(BaseModel):
    source: str
    user: User