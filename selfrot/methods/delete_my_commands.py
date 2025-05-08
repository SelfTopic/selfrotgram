from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import BotCommandScope

@dataclass
class DeleteMyCommands(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteMyCommands"
    scope: Optional[BotCommandScope] = None
    language_code: Optional[str] = None