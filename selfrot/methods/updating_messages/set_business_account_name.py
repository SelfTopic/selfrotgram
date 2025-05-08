from typing import Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetBusinessAccountName(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setBusinessAccountName"
    business_connection_id: str
    first_name: str
    last_name: Optional[str] = None