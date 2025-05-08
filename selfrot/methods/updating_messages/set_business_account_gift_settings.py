from typing import ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import AcceptedGiftTypes

@dataclass
class SetBusinessAccountGiftSettings(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setBusinessAccountGiftSettings"
    business_connection_id: str
    show_gift_button: bool
    accepted_gift_types: AcceptedGiftTypes