from typing import ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class DeleteStory(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteStory"
    business_connection_id: str
    story_id: int