from typing import Optional
from pydantic import BaseModel
from .user import User
from .unique_gift import UniqueGift

class OwnedGiftUnique(BaseModel):
    type: str
    gift: UniqueGift
    owned_gift_id: Optional[str] = None
    sender_user: Optional[User] = None
    send_date: int
    is_saved: Optional[bool] = None
    can_be_transferred: Optional[bool] = None
    transfer_star_count: Optional[int] = None