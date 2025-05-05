from typing import List
from pydantic import BaseModel
from .inline_keyboard_button import InlineKeyboardButton


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: List[List[InlineKeyboardButton]]