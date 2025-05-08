from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class EditForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editForumTopic"
    chat_id: Union[int, str]
    message_thread_id: int
    name: Optional[str] = None
    icon_custom_emoji_id: Optional[str] = None