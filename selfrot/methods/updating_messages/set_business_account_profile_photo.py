from typing import Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import InputProfilePhoto

@dataclass
class SetBusinessAccountProfilePhoto(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setBusinessAccountProfilePhoto"
    business_connection_id: str
    photo: InputProfilePhoto
    is_public: Optional[bool] = None