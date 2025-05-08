from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class HideGeneralForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "hideGeneralForumTopic"
    chat_id: Union[int, str]