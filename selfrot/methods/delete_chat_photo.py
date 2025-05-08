from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class DeleteChatPhoto(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteChatPhoto"
    chat_id: Union[int, str]