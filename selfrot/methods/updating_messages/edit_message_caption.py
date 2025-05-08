from typing import Union, List, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import InlineKeyboardMarkup
from ..types import MessageEntity

@dataclass
class EditMessageCaption(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editMessageCaption"
    business_connection_id: Optional[str] = None
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None