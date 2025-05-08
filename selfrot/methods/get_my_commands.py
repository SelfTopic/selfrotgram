from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import BotCommandScope

@dataclass
class GetMyCommands(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMyCommands"
    scope: Optional[BotCommandScope] = None
    language_code: Optional[str] = None