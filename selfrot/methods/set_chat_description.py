from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetChatDescription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatDescription"
    chat_id: Union[int, str]
    description: Optional[str] = None