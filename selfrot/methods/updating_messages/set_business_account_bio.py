from typing import Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetBusinessAccountBio(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setBusinessAccountBio"
    business_connection_id: str
    bio: Optional[str] = None