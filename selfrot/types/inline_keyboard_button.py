from typing import Optional
from pydantic import BaseModel
from .copy_text_button import CopyTextButton
from .switch_inline_query_chosen_chat import SwitchInlineQueryChosenChat
from .login_url import LoginUrl
from .web_app_info import WebAppInfo
from ..games import CallbackGame

class InlineKeyboardButton(BaseModel):
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None
    web_app: Optional[WebAppInfo] = None
    login_url: Optional[LoginUrl] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    switch_inline_query_chosen_chat: Optional[SwitchInlineQueryChosenChat] = None
    copy_text: Optional[CopyTextButton] = None
    callback_game: Optional[CallbackGame] = None
    pay: Optional[bool] = None