from typing import List, Optional
from pydantic import BaseModel
from .input_message_content import InputMessageContent
from ..types import InlineKeyboardMarkup
from ..types import MessageEntity

class InlineQueryResultCachedVoice(BaseModel):
    type: str
    id: str
    voice_file_id: str
    title: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None