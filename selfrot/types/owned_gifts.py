from typing import List, Optional
from pydantic import BaseModel
from .owned_gift import OwnedGift

class OwnedGifts(BaseModel):
    total_count: int
    gifts: List[OwnedGift]
    next_offset: Optional[str] = None