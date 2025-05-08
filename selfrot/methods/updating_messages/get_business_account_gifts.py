from typing import Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetBusinessAccountGifts(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getBusinessAccountGifts"
    business_connection_id: str
    exclude_unsaved: Optional[bool] = None
    exclude_saved: Optional[bool] = None
    exclude_unlimited: Optional[bool] = None
    exclude_limited: Optional[bool] = None
    exclude_unique: Optional[bool] = None
    sort_by_price: Optional[bool] = None
    offset: Optional[str] = None
    limit: Optional[int] = None