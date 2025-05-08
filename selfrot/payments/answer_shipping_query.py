from typing import List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from .shipping_option import ShippingOption

@dataclass
class AnswerShippingQuery(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "answerShippingQuery"
    shipping_query_id: str
    ok: bool
    shipping_options: Optional[List[ShippingOption]] = None
    error_message: Optional[str] = None