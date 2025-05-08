from typing import Optional
from pydantic import BaseModel
from ..stickers import Sticker

class Gift(BaseModel):
    id: str
    sticker: Sticker
    star_count: int
    upgrade_star_count: Optional[int] = None
    total_count: Optional[int] = None
    remaining_count: Optional[int] = None