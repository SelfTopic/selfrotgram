from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class RevokeChatInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "revokeChatInviteLink"
    chat_id: Union[int, str]
    invite_link: str