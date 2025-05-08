from typing import Union, List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import MessageEntity
from ..types import InlineKeyboardMarkup
from ..types import ReplyKeyboardMarkup
from ..types import ReplyKeyboardRemove
from ..types import InputFile
from ..types import ForceReply
from ..types import ReplyParameters

@dataclass
class SendAudio(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendAudio"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    audio: Union[InputFile, str]
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    duration: Optional[int] = None
    performer: Optional[str] = None
    title: Optional[str] = None
    thumbnail: Optional[Union[InputFile, str]] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None