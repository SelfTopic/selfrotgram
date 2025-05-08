from typing import Union, List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import MessageEntity
from ..types import InlineKeyboardMarkup
from ..types import ReplyKeyboardMarkup
from ..types import LinkPreviewOptions
from ..types import ReplyKeyboardRemove
from ..types import ForceReply
from ..types import ReplyParameters

@dataclass
class SendMessage(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendMessage"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    text: str
    parse_mode: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None