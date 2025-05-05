from typing import List, Optional
from pydantic import BaseModel
from .gift import Gift
from .user import User
from .message_entity import MessageEntity

class OwnedGiftRegular(BaseModel):
    type: str
    gift: Gift
    owned_gift_id: Optional[str] = None
    sender_user: Optional[User] = None
    send_date: int
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    is_private: Optional[bool] = None
    is_saved: Optional[bool] = None
    can_be_upgraded: Optional[bool] = None
    was_refunded: Optional[bool] = None
    convert_star_count: Optional[int] = None
    prepaid_upgrade_star_count: Optional[int] = None