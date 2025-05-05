from pydantic import BaseModel
from .user import User

class ChatBoostSourcePremium(BaseModel):
    source: str
    user: User