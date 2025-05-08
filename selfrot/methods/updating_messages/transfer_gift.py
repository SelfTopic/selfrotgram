from typing import Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class TransferGift(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "transferGift"
    business_connection_id: str
    owned_gift_id: str
    new_owner_chat_id: int
    star_count: Optional[int] = None