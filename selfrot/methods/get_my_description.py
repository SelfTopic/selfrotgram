from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetMyDescription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMyDescription"
    language_code: Optional[str] = None