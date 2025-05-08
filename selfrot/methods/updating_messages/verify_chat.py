from typing import Union, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class VerifyChat(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "verifyChat"
    chat_id: Union[int, str]
    custom_description: Optional[str] = None