from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetMyName(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMyName"
    name: Optional[str] = None
    language_code: Optional[str] = None