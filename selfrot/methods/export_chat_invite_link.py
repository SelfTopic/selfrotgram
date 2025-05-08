from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class ExportChatInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "exportChatInviteLink"
    chat_id: Union[int, str]