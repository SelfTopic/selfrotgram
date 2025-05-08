from typing import List, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import MessageEntity

@dataclass
class GiftPremiumSubscription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "giftPremiumSubscription"
    user_id: int
    month_count: int
    star_count: int
    text: Optional[str] = None
    text_parse_mode: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None