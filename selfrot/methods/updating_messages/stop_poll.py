from typing import Union, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import InlineKeyboardMarkup

@dataclass
class StopPoll(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "stopPoll"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_id: int
    reply_markup: Optional[InlineKeyboardMarkup] = None