from typing import Optional
from pydantic import BaseModel, Field
from .order_info import OrderInfo
from ..types import User

class PreCheckoutQuery(BaseModel):
    id: str
    user: User = Field(alias="from")
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None