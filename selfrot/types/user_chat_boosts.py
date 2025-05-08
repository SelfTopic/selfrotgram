from typing import List
from pydantic import BaseModel
from .chat_boost import ChatBoost

class UserChatBoosts(BaseModel):
    boosts: List[ChatBoost]