from typing import ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class ConvertGiftToStars(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "convertGiftToStars"
    business_connection_id: str
    owned_gift_id: str