from typing import Union, List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import MessageEntity
from ..types import InlineKeyboardMarkup
from ..types import ReplyKeyboardMarkup
from ..types import InputPollOption
from ..types import ReplyKeyboardRemove
from ..types import ForceReply
from ..types import ReplyParameters

@dataclass
class SendPoll(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendPoll"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    question: str
    question_parse_mode: Optional[str] = None
    question_entities: Optional[List[MessageEntity]] = None
    options: List[InputPollOption]
    is_anonymous: Optional[bool] = None
    type: Optional[str] = None
    allows_multiple_answers: Optional[bool] = None
    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None
    explanation_parse_mode: Optional[str] = None
    explanation_entities: Optional[List[MessageEntity]] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None
    is_closed: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None