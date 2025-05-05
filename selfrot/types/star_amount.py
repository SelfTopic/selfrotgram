from typing import Optional
from pydantic import BaseModel


class StarAmount(BaseModel):
    amount: int
    nanostar_amount: Optional[int] = None