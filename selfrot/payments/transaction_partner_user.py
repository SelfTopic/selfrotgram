from typing import List, Optional
from pydantic import BaseModel
from ..types import PaidMedia
from ..types import Gift
from .affiliate_info import AffiliateInfo
from ..types import User

class TransactionPartnerUser(BaseModel):
    type: str
    transaction_type: str
    user: User
    affiliate: Optional[AffiliateInfo] = None
    invoice_payload: Optional[str] = None
    subscription_period: Optional[int] = None
    paid_media: Optional[List[PaidMedia]] = None
    paid_media_payload: Optional[str] = None
    gift: Optional[Gift] = None
    premium_subscription_duration: Optional[int] = None