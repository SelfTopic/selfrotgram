from dataclasses import dataclass 
from ..methods import TelegramAPIMethod
from typing import Any

@dataclass 
class TelegramAPIServer:

    url: str 
    data: dict[str, Any]

    def __init__(self, url: str):
        self.url = url

    def get_url(
        self,
        token: str,
        method: TelegramAPIMethod
    ):
        return self.url.format(token=token, method=method.__api_method__)
    
    def build_data(
        self,
        method: TelegramAPIMethod
    ):
        pass

TELEGRAM_API = TelegramAPIServer(url="https://api.telegram.org/bot{token}/{method}")