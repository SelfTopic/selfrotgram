from typing import List, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class DeleteBusinessMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteBusinessMessages"
    business_connection_id: str
    message_ids: List[int]