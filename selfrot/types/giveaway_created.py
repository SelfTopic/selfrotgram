from typing import Optional
from pydantic import BaseModel


class GiveawayCreated(BaseModel):
    prize_star_count: Optional[int] = None