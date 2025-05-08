from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetFile(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getFile"
    file_id: str