from typing import List, Optional
from pydantic import BaseModel
from .array of _keyboard_button import Array of KeyboardButton

class ReplyKeyboardMarkup(BaseModel):
    keyboard: List[Array of KeyboardButton]
    is_persistent: Optional[bool] = None
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None