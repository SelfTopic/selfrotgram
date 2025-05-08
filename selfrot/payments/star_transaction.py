from typing import Optional
from pydantic import BaseModel
from .transaction_partner import TransactionPartner

class StarTransaction(BaseModel):
    id: str
    amount: int
    nanostar_amount: Optional[int] = None
    date: int
    source: Optional[TransactionPartner] = None
    receiver: Optional[TransactionPartner] = None