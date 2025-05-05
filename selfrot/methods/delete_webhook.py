from typing import ClassVar
from .base import TelegramAPIMethod
from dataclasses import dataclass


@dataclass
class DeleteWebhook(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteWebhook"