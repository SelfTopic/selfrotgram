from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetBusinessConnection(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getBusinessConnection"
    business_connection_id: str