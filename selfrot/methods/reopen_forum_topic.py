from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class ReopenForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "reopenForumTopic"
    chat_id: Union[int, str]
    message_thread_id: int