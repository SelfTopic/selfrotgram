from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class ForwardMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "forwardMessage"
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    from_chat_id: Union[int, str]
    video_start_timestamp: Optional[int] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    message_id: int