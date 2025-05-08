from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetChatMenuButton(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getChatMenuButton"
    chat_id: Optional[int] = None