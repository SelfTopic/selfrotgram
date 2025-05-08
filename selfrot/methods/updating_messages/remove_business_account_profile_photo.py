from typing import Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class RemoveBusinessAccountProfilePhoto(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "removeBusinessAccountProfilePhoto"
    business_connection_id: str
    is_public: Optional[bool] = None