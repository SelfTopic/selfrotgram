from typing import List
from pydantic import BaseModel


class UserChatBoosts(BaseModel):
    boosts: List[ChatBoost]