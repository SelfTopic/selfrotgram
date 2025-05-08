from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class EditChatSubscriptionInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editChatSubscriptionInviteLink"
    chat_id: Union[int, str]
    invite_link: str
    name: Optional[str] = None