from typing import List, Optional
from pydantic import BaseModel
from .message_entity import MessageEntity
from .gift import Gift

class GiftInfo(BaseModel):
    gift: Gift
    owned_gift_id: Optional[str] = None
    convert_star_count: Optional[int] = None
    prepaid_upgrade_star_count: Optional[int] = None
    can_be_upgraded: Optional[bool] = None
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    is_private: Optional[bool] = None