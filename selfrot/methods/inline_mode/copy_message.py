from typing import Union, List, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import MessageEntity
from ..types import ReplyKeyboardRemove
from ..types import InlineKeyboardMarkup
from ..types import ReplyKeyboardMarkup
from ..types import ReplyParameters
from ..types import ForceReply

@dataclass
class CopyMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "copyMessage"
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    from_chat_id: Union[int, str]
    message_id: int
    video_start_timestamp: Optional[int] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None