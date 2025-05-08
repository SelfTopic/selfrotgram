from typing import Union, List, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class ForwardMessages(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "forwardMessages"
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    from_chat_id: Union[int, str]
    message_ids: List[int]
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None