from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class LeaveChat(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "leaveChat"
    chat_id: Union[int, str]