from typing import Union, List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import ReplyParameters
from ..types import InlineKeyboardMarkup
from .labeled_price import LabeledPrice

@dataclass
class SendInvoice(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendInvoice"
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    title: str
    description: str
    payload: str
    provider_token: Optional[str] = None
    currency: str
    prices: List[LabeledPrice]
    max_tip_amount: Optional[int] = None
    suggested_tip_amounts: Optional[List[int]] = None
    start_parameter: Optional[str] = None
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
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None