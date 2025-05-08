from typing import List, Optional
from pydantic import BaseModel
from .input_message_content import InputMessageContent
from ..types import InlineKeyboardMarkup
from ..types import MessageEntity

class InlineQueryResultAudio(BaseModel):
    type: str
    id: str
    audio_url: str
    title: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    performer: Optional[str] = None
    audio_duration: Optional[int] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None