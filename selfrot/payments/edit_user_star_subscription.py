from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class EditUserStarSubscription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editUserStarSubscription"
    user_id: int
    telegram_payment_charge_id: str
    is_canceled: bool