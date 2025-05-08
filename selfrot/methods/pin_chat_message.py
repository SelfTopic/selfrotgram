from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class PinChatMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "pinChatMessage"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_id: int
    disable_notification: Optional[bool] = None