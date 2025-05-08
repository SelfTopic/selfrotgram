from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class EditGeneralForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editGeneralForumTopic"
    chat_id: Union[int, str]
    name: str