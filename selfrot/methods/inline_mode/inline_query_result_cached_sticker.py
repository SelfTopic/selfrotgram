from typing import Optional
from pydantic import BaseModel
from .input_message_content import InputMessageContent
from ..types import InlineKeyboardMarkup

class InlineQueryResultCachedSticker(BaseModel):
    type: str
    id: str
    sticker_file_id: str
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None