from typing import Optional
from pydantic import BaseModel


class UniqueGiftInfo(BaseModel):
    gift: UniqueGift
    origin: str
    owned_gift_id: Optional[str] = None
    transfer_star_count: Optional[int] = None