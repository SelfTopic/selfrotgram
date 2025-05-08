from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import ReplyKeyboardRemove
from ..types import ReplyParameters
from ..types import InlineKeyboardMarkup
from ..types import InputFile
from ..types import ForceReply
from ..types import ReplyKeyboardMarkup

@dataclass
class SendSticker(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendSticker"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    sticker: Union[InputFile, str]
    emoji: Optional[str] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None