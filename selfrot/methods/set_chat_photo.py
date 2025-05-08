from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import InputFile

@dataclass
class SetChatPhoto(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatPhoto"
    chat_id: Union[int, str]
    photo: InputFile