from typing import Union, List, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import MessageEntity

@dataclass
class SendGift(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendGift"
    user_id: Optional[int] = None
    chat_id: Optional[Union[int, str]] = None
    gift_id: str
    pay_for_upgrade: Optional[bool] = None
    text: Optional[str] = None
    text_parse_mode: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None