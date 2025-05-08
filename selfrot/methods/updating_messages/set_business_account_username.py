from typing import Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetBusinessAccountUsername(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setBusinessAccountUsername"
    business_connection_id: str
    username: Optional[str] = None