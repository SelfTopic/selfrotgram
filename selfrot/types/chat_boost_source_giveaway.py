from typing import Optional
from pydantic import BaseModel
from .user import User

class ChatBoostSourceGiveaway(BaseModel):
    source: str
    giveaway_message_id: int
    user: Optional[User] = None
    prize_star_count: Optional[int] = None
    is_unclaimed: Optional[bool] = None