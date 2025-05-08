from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import MenuButton

@dataclass
class SetChatMenuButton(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatMenuButton"
    chat_id: Optional[int] = None
    menu_button: Optional[MenuButton] = None