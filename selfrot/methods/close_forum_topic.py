from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class CloseForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "closeForumTopic"
    chat_id: Union[int, str]
    message_thread_id: int