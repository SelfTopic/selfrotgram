from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import ChatPermissions

@dataclass
class RestrictChatMember(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "restrictChatMember"
    chat_id: Union[int, str]
    user_id: int
    permissions: ChatPermissions
    use_independent_chat_permissions: Optional[bool] = None
    until_date: Optional[int] = None