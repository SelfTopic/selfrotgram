from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class ReopenGeneralForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "reopenGeneralForumTopic"
    chat_id: Union[int, str]