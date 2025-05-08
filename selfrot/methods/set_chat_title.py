from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetChatTitle(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatTitle"
    chat_id: Union[int, str]
    title: str