from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetMyDescription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMyDescription"
    description: Optional[str] = None
    language_code: Optional[str] = None