from dataclasses import dataclass
from typing import Any

from ..methods.base import TelegramMethod


@dataclass
class TelegramAPIServer:
    url: str

    def get_url(self, token: str, method: TelegramMethod[Any]) -> str:
        return self.url.format(token=token, method=method.__api_method__)


@dataclass
class TelegramFileServer:
    """Скачивание файлов: отдельный URL, не тот же, что у вызова методов."""

    url: str

    def get_url(self, token: str, file_path: str) -> str:
        return self.url.format(token=token, file_path=file_path)


TELEGRAM_API = TelegramAPIServer(url="https://api.telegram.org/bot{token}/{method}")
TELEGRAM_FILE_API = TelegramFileServer(
    url="https://api.telegram.org/file/bot{token}/{file_path}"
)
