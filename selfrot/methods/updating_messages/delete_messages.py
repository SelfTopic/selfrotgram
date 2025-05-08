from typing import Union, List, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class DeleteMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteMessages"
    chat_id: Union[int, str]
    message_ids: List[int]