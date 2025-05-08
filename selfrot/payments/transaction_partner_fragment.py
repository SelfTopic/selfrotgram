from typing import Optional
from pydantic import BaseModel
from .revenue_withdrawal_state import RevenueWithdrawalState

class TransactionPartnerFragment(BaseModel):
    type: str
    withdrawal_state: Optional[RevenueWithdrawalState] = None