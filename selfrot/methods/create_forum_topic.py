from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class CreateForumTopic(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "createForumTopic"
    chat_id: Union[int, str]
    name: str
    icon_color: Optional[int] = None
    icon_custom_emoji_id: Optional[str] = None