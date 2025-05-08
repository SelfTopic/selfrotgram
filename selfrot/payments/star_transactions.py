from typing import List
from pydantic import BaseModel
from .star_transaction import StarTransaction

class StarTransactions(BaseModel):
    transactions: List[StarTransaction]