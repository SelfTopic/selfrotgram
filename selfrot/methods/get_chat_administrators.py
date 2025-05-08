from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetChatAdministrators(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getChatAdministrators"
    chat_id: Union[int, str]