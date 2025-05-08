from typing import List, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from .inline_query_results_button import InlineQueryResultsButton
from .inline_query_result import InlineQueryResult

@dataclass
class AnswerInlineQuery(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "answerInlineQuery"
    inline_query_id: str
    results: List[InlineQueryResult]
    cache_time: Optional[int] = None
    is_personal: Optional[bool] = None
    next_offset: Optional[str] = None
    button: Optional[InlineQueryResultsButton] = None