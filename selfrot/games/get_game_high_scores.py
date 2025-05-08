from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass


@dataclass
class GetGameHighScores(TelegramAPIMethod):
	__api_method__: ClassVar[str] = "getGameHighScores"
	user_id: int
	chat_id: Optional[int] = None
	message_id: Optional[int] = None
	inline_message_id: Optional[str] = None