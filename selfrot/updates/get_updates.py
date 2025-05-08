from typing import List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetUpdates(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getUpdates"
    offset: Optional[int] = None
    limit: Optional[int] = None
    timeout: Optional[int] = None
    allowed_updates: Optional[List[str]] = None