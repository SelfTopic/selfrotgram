from typing import ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetBusinessAccountStarBalance(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getBusinessAccountStarBalance"
    business_connection_id: str