from typing import Optional
from pydantic import BaseModel
from ..types import Chat
from ..types import User

class AffiliateInfo(BaseModel):
    affiliate_user: Optional[User] = None
    affiliate_chat: Optional[Chat] = None
    commission_per_mille: int
    amount: int
    nanostar_amount: Optional[int] = None