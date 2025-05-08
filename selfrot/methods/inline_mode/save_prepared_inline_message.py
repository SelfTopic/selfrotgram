from typing import Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from .inline_query_result import InlineQueryResult

@dataclass
class SavePreparedInlineMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "savePreparedInlineMessage"
    user_id: int
    result: InlineQueryResult
    allow_user_chats: Optional[bool] = None
    allow_bot_chats: Optional[bool] = None
    allow_group_chats: Optional[bool] = None
    allow_channel_chats: Optional[bool] = None