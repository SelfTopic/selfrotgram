from typing import List, Optional
from pydantic import BaseModel
from .input_message_content import InputMessageContent
from ..types import InlineKeyboardMarkup
from ..types import MessageEntity

class InlineQueryResultCachedVideo(BaseModel):
    type: str
    id: str
    video_file_id: str
    title: str
    description: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None