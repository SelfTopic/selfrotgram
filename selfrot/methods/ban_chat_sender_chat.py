from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class BanChatSenderChat(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "banChatSenderChat"
    chat_id: Union[int, str]
    sender_chat_id: int