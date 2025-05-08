from typing import Union, Self
from pydantic import BaseModel
from .unique_gift_backdrop_colors import UniqueGiftBackdropColors

class UniqueGiftBackdrop(BaseModel):
    name: str
    colors: Union[UniqueGiftBackdropColors]
    rarity_per_mille: int