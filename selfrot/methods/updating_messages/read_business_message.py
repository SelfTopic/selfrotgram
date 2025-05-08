from typing import ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class ReadBusinessMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "readBusinessMessage"
    business_connection_id: str
    chat_id: int
    message_id: int