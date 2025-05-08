from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetMyShortDescription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMyShortDescription"
    language_code: Optional[str] = None