from typing import List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import BotCommand
from ..types import BotCommandScope

@dataclass
class SetMyCommands(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMyCommands"
    commands: List[BotCommand]
    scope: Optional[BotCommandScope] = None
    language_code: Optional[str] = None