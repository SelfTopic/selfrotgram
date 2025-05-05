from typing import ClassVar
from .base import TelegramAPIMethod 
from dataclasses import dataclass


@dataclass
class GetUpdates(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getUpdates"
    offset: int