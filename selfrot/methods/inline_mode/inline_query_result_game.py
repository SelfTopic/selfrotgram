from typing import Optional
from pydantic import BaseModel
from ..types import InlineKeyboardMarkup

class InlineQueryResultGame(BaseModel):
    type: str
    id: str
    game_short_name: str
    reply_markup: Optional[InlineKeyboardMarkup] = None