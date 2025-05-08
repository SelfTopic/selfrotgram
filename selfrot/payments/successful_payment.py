from typing import Optional
from pydantic import BaseModel
from .order_info import OrderInfo

class SuccessfulPayment(BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    subscription_expiration_date: Optional[int] = None
    is_recurring: Optional[bool] = None
    is_first_recurring: Optional[bool] = None
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None
    telegram_payment_charge_id: str
    provider_payment_charge_id: str