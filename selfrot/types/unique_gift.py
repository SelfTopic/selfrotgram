from pydantic import BaseModel
from .unique_gift_backdrop import UniqueGiftBackdrop
from .unique_gift_model import UniqueGiftModel
from .unique_gift_symbol import UniqueGiftSymbol

class UniqueGift(BaseModel):
    base_name: str
    name: str
    number: int
    model: UniqueGiftModel
    symbol: UniqueGiftSymbol
    backdrop: UniqueGiftBackdrop