from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class AnswerCallbackQuery(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "answerCallbackQuery"
    callback_query_id: str
    text: Optional[str] = None
    show_alert: Optional[bool] = None
    url: Optional[str] = None
    cache_time: Optional[int] = None