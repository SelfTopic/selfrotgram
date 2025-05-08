from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class RefundStarPayment(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "refundStarPayment"
    user_id: int
    telegram_payment_charge_id: str