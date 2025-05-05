from pydantic import BaseModel
from ..stickers.sticker import Sticker

class UniqueGiftModel(BaseModel):
    name: str
    sticker: Sticker
    rarity_per_mille: int