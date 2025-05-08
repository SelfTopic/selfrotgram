from typing import Union, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class RemoveChatVerification(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "removeChatVerification"
    chat_id: Union[int, str]