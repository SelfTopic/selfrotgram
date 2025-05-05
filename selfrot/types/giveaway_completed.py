from typing import Optional
from pydantic import BaseModel
from .message import Message

class GiveawayCompleted(BaseModel):
    winner_count: int
    unclaimed_prize_count: Optional[int] = None
    giveaway_message: Optional[Message] = None
    is_star_giveaway: Optional[bool] = None