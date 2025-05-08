from typing import Optional
from pydantic import BaseModel
from .input_message_content import InputMessageContent
from ..types import InlineKeyboardMarkup

class InlineQueryResultArticle(BaseModel):
    type: str
    id: str
    title: str
    input_message_content: InputMessageContent
    reply_markup: Optional[InlineKeyboardMarkup] = None
    url: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    thumbnail_width: Optional[int] = None
    thumbnail_height: Optional[int] = None