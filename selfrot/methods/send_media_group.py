from typing import Union, List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from .input_media_photo and _input_media_video import InputMediaPhoto and InputMediaVideo
from ..types import ReplyParameters
from ..types import InputMediaDocument
from ..types import InputMediaAudio

@dataclass
class SendMediaGroup(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendMediaGroup"
    business_connection_id: Optional[str] = None
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    media: List[InputMediaAudio, InputMediaDocument, InputMediaPhoto and InputMediaVideo]
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None