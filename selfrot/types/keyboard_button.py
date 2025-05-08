from typing import Optional, Self
from pydantic import BaseModel
from .keyboard_button_poll_type import KeyboardButtonPollType
from .keyboard_button_request_users import KeyboardButtonRequestUsers
from .keyboard_button_request_chat import KeyboardButtonRequestChat
from .web_app_info import WebAppInfo

class KeyboardButton(BaseModel):
    text: str
    request_users: Optional[KeyboardButtonRequestUsers] = None
    request_chat: Optional[KeyboardButtonRequestChat] = None
    request_contact: Optional[bool] = None
    request_location: Optional[bool] = None
    request_poll: Optional[KeyboardButtonPollType] = None
    web_app: Optional[WebAppInfo] = None