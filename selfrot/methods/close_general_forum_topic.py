from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class CloseGeneralForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "closeGeneralForumTopic"
    chat_id: Union[int, str]