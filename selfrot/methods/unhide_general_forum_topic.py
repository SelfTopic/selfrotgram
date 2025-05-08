from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class UnhideGeneralForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unhideGeneralForumTopic"
    chat_id: Union[int, str]