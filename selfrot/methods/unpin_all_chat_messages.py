from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class UnpinAllChatMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unpinAllChatMessages"
    chat_id: Union[int, str]