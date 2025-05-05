from typing import List, Optional
from pydantic import BaseModel
from .user import User

class GiveawayWinners(BaseModel):
    chat: Chat
    giveaway_message_id: int
    winners_selection_date: int
    winner_count: int
    winners: List[User]
    additional_chat_count: Optional[int] = None
    prize_star_count: Optional[int] = None
    premium_subscription_month_count: Optional[int] = None
    unclaimed_prize_count: Optional[int] = None
    only_new_members: Optional[bool] = None
    was_refunded: Optional[bool] = None
    prize_description: Optional[str] = None