from typing import ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class RemoveUserVerification(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "removeUserVerification"
    user_id: int