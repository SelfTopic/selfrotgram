from dataclasses import dataclass
from typing import Any

from ..methods.base import TelegramMethod


@dataclass
class TelegramAPIServer:
    url: str

    def get_url(self, token: str, method: TelegramMethod[Any]) -> str:
        return self.url.format(token=token, method=method.__api_method__)


TELEGRAM_API = TelegramAPIServer(url="https://api.telegram.org/bot{token}/{method}")
