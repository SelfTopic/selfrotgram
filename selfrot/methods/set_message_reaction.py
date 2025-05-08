from typing import Union, List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import ReactionType

@dataclass
class SetMessageReaction(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMessageReaction"
    chat_id: Union[int, str]
    message_id: int
    reaction: Optional[List[ReactionType]] = None
    is_big: Optional[bool] = None