from typing import List, Optional
from pydantic import BaseModel
from .keyboard_button import KeyboardButton


class ReplyKeyboardMarkup(BaseModel):
    keyboard: List[List[KeyboardButton]]
    is_persistent: Optional[bool] = None
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None