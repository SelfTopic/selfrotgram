from typing import ClassVar 
from .base import TelegramAPIMethod
from dataclasses import dataclass


@dataclass
class SendMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendMessage"
    chat_id: int
    user_id: int
    text: str