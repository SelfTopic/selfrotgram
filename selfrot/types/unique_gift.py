from typing import Self
from pydantic import BaseModel
from .unique_gift_symbol import UniqueGiftSymbol
from .unique_gift_backdrop import UniqueGiftBackdrop
from .unique_gift_model import UniqueGiftModel

class UniqueGift(BaseModel):
    base_name: str
    name: str
    number: int
    model: UniqueGiftModel
    symbol: UniqueGiftSymbol
    backdrop: UniqueGiftBackdrop