from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetChatMember(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getChatMember"
    chat_id: Union[int, str]
    user_id: int