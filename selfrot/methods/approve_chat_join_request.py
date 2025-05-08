from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class ApproveChatJoinRequest(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "approveChatJoinRequest"
    chat_id: Union[int, str]
    user_id: int