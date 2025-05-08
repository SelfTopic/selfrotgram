from typing import Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class UpgradeGift(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "upgradeGift"
    business_connection_id: str
    owned_gift_id: str
    keep_original_details: Optional[bool] = None
    star_count: Optional[int] = None