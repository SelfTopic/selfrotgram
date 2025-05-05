from typing import List
from pydantic import BaseModel
from .paid_media import PaidMedia

class PaidMediaInfo(BaseModel):
    star_count: int
    paid_media: List[PaidMedia]