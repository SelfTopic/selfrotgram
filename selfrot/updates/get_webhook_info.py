from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetWebhookInfo(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getWebhookInfo"