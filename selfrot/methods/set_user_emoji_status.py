from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetUserEmojiStatus(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setUserEmojiStatus"
    user_id: int
    emoji_status_custom_emoji_id: Optional[str] = None
    emoji_status_expiration_date: Optional[int] = None