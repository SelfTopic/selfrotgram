from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetMyShortDescription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMyShortDescription"
    short_description: Optional[str] = None
    language_code: Optional[str] = None