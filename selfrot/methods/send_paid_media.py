from typing import Union, List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import MessageEntity
from ..types import InlineKeyboardMarkup
from ..types import ReplyKeyboardMarkup
from ..types import ReplyKeyboardRemove
from ..types import ForceReply
from ..types import InputPaidMedia
from ..types import ReplyParameters

@dataclass
class SendPaidMedia(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendPaidMedia"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    star_count: int
    media: List[InputPaidMedia]
    payload: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None