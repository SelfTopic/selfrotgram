from pydantic import BaseModel

class RevenueWithdrawalStateSucceeded(BaseModel):
    type: str
    date: int
    url: str