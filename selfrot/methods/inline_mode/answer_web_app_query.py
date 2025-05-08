from typing import ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from .inline_query_result import InlineQueryResult

@dataclass
class AnswerWebAppQuery(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "answerWebAppQuery"
    web_app_query_id: str
    result: InlineQueryResult