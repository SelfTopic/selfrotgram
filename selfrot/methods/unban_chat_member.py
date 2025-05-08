from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class UnbanChatMember(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "unbanChatMember"
    chat_id: Union[int, str]
    user_id: int
    only_if_banned: Optional[bool] = None