from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class DeclineChatJoinRequest(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "declineChatJoinRequest"
    chat_id: Union[int, str]
    user_id: int