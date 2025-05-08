from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetChatAdministratorCustomTitle(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatAdministratorCustomTitle"
    chat_id: Union[int, str]
    user_id: int
    custom_title: str