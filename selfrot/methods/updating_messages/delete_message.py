from typing import Union, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class DeleteMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteMessage"
    chat_id: Union[int, str]
    message_id: int