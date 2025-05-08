from typing import ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from .class_var[str] import ClassVar[str]

from typing import ClassVar
from .base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetMe(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMe"