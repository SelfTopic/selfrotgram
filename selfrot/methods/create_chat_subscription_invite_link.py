from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class CreateChatSubscriptionInviteLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "createChatSubscriptionInviteLink"
    chat_id: Union[int, str]
    name: Optional[str] = None
    subscription_period: int
    subscription_price: int