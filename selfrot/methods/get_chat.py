from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetChat(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getChat"
    chat_id: Union[int, str]