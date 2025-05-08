from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class DeleteWebhook(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteWebhook"
    drop_pending_updates: Optional[bool] = None