from typing import List, Optional
from pydantic import BaseModel
from .message_entity import MessageEntity
from .user import User
from .gift import Gift

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