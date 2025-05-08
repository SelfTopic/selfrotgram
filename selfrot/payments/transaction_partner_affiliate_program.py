from typing import Optional
from pydantic import BaseModel
from ..types import User

class TransactionPartnerAffiliateProgram(BaseModel):
    type: str
    sponsor_user: Optional[User] = None
    commission_per_mille: int