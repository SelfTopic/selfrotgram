from typing import Union, Optional, ClassVar
from ..methods.base import TelegramAPIMethod
from pydantic import BaseModel
from dataclasses import dataclass
from ..types.force_reply import ForceReply
from ..types.input_file import InputFile
from ..types.reply_parameters import ReplyParameters
from ..types.reply_keyboard_markup import ReplyKeyboardMarkup
from ..types.inline_keyboard_markup import InlineKeyboardMarkup
from ..types.reply_keyboard_remove import ReplyKeyboardRemove

@dataclass
class SendSticker(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendSticker"
    chat_id: Union[int, str]
    sticker: Union[InputFile, str]
    business_connection_id: Optional[str] = None
    message_thread_id: Optional[int] = None
    emoji: Optional[str] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None