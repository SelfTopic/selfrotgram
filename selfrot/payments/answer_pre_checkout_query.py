from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class AnswerPreCheckoutQuery(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "answerPreCheckoutQuery"
    pre_checkout_query_id: str
    ok: bool
    error_message: Optional[str] = None