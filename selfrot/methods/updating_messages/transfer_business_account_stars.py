from typing import ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class TransferBusinessAccountStars(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "transferBusinessAccountStars"
    business_connection_id: str
    star_count: int