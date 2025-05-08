from typing import List, Optional
from pydantic import BaseModel
from ..types import LinkPreviewOptions
from ..types import MessageEntity

class InputTextMessageContent(BaseModel):
    message_text: str
    parse_mode: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    link_preview_options: Optional[LinkPreviewOptions] = None