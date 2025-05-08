from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class UnpinAllGeneralForumTopicMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unpinAllGeneralForumTopicMessages"
    chat_id: Union[int, str]