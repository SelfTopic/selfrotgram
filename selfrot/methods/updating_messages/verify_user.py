from typing import Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class VerifyUser(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "verifyUser"
    user_id: int
    custom_description: Optional[str] = None