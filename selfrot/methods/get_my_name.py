from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetMyName(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMyName"
    language_code: Optional[str] = None