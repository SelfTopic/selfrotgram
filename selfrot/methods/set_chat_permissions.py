from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import ChatPermissions

@dataclass
class SetChatPermissions(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatPermissions"
    chat_id: Union[int, str]
    permissions: ChatPermissions
    use_independent_chat_permissions: Optional[bool] = None