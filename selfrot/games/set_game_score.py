from typing import Optional, ClassVar
from ..methods.base import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetGameScore(TelegramAPIMethod):
	__api_method__: ClassVar[str] = "setGameScore"
	user_id: int
	score: int
	force: Optional[bool] = None
	disable_edit_message: Optional[bool] = None
	chat_id: Optional[int] = None
	message_id: Optional[int] = None
	inline_message_id: Optional[str] = None