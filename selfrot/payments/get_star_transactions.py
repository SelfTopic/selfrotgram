from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetStarTransactions(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getStarTransactions"
    offset: Optional[int] = None
    limit: Optional[int] = None