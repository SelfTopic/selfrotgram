from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class CreateChatInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "createChatInviteLink"
    chat_id: Union[int, str]
    name: Optional[str] = None
    expire_date: Optional[int] = None
    member_limit: Optional[int] = None
    creates_join_request: Optional[bool] = None