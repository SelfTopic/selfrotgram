from typing import Union, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import InlineKeyboardMarkup
from ..types import InputMedia

@dataclass
class EditMessageMedia(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editMessageMedia"
    business_connection_id: Optional[str] = None
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    media: InputMedia
    reply_markup: Optional[InlineKeyboardMarkup] = None