from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetChatMemberCount(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getChatMemberCount"
    chat_id: Union[int, str]