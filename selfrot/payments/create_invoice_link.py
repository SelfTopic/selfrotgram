from typing import List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from .labeled_price import LabeledPrice

@dataclass
class CreateInvoiceLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "createInvoiceLink"
    business_connection_id: Optional[str] = None
    title: str
    description: str
    payload: str
    provider_token: Optional[str] = None
    currency: str
    prices: List[LabeledPrice]
    subscription_period: Optional[int] = None
    max_tip_amount: Optional[int] = None
    suggested_tip_amounts: Optional[List[int]] = None
    provider_data: Optional[str] = None
    photo_url: Optional[str] = None
    photo_size: Optional[int] = None
    photo_width: Optional[int] = None
    photo_height: Optional[int] = None
    need_name: Optional[bool] = None
    need_phone_number: Optional[bool] = None
    need_email: Optional[bool] = None
    need_shipping_address: Optional[bool] = None
    send_phone_number_to_provider: Optional[bool] = None
    send_email_to_provider: Optional[bool] = None
    is_flexible: Optional[bool] = None