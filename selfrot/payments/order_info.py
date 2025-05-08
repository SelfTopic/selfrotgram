from typing import Optional
from pydantic import BaseModel
from .shipping_address import ShippingAddress

class OrderInfo(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    shipping_address: Optional[ShippingAddress] = None