from typing import Union, List, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import InlineKeyboardMarkup
from ..types import LinkPreviewOptions
from ..types import MessageEntity

@dataclass
class EditMessageText(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editMessageText"
    business_connection_id: Optional[str] = None
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    text: str
    parse_mode: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None