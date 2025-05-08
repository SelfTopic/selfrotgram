from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import ReplyParameters
# from ..types.inline_keyboard_markup import InlineKeyboardMarkup


@dataclass
class SendGame(TelegramAPIMethod):
	__api_method__: ClassVar[str] = "sendGame"
	chat_id: int
	game_short_name: str
	business_connection_id: Optional[str] = None
	message_thread_id: Optional[int] = None
	disable_notification: Optional[bool] = None
	protect_content: Optional[bool] = None
	allow_paid_broadcast: Optional[bool] = None
	message_effect_id: Optional[str] = None
	reply_parameters: Optional[ReplyParameters] = None
	# reply_markup: Optional[InlineKeyboardMarkup] = None