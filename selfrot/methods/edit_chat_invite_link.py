from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class EditChatInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editChatInviteLink"
    chat_id: Union[int, str]
    invite_link: str
    name: Optional[str] = None
    expire_date: Optional[int] = None
    member_limit: Optional[int] = None
    creates_join_request: Optional[bool] = None