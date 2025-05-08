from typing import List
from pydantic import BaseModel
from .labeled_price import LabeledPrice

class ShippingOption(BaseModel):
    id: str
    title: str
    prices: List[LabeledPrice]