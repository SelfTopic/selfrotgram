from typing import List
from pydantic import BaseModel
from .array of _inline_keyboard_button import Array of InlineKeyboardButton

class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: List[Array of InlineKeyboardButton]