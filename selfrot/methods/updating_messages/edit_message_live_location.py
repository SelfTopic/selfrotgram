from typing import Union, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import InlineKeyboardMarkup

@dataclass
class EditMessageLiveLocation(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editMessageLiveLocation"
    business_connection_id: Optional[str] = None
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    latitude: float
    longitude: float
    live_period: Optional[int] = None
    horizontal_accuracy: Optional[float] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None