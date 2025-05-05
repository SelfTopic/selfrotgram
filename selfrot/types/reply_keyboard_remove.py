from typing import Optional
from pydantic import BaseModel


class ReplyKeyboardRemove(BaseModel):
    remove_keyboard: bool
    selective: Optional[bool] = None