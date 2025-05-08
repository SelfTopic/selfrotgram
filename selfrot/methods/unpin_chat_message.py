from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class UnpinChatMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unpinChatMessage"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_id: Optional[int] = None