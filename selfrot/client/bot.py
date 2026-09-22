import asyncio
import logging
import re
from typing import Any, TypeVar

from pydantic import TypeAdapter

from ..config import ConfigAPI
from ..exceptions import (
    ConfigError,
    FileNotAvailableError,
    TelegramAPIError,
    TelegramRetryAfter,
)
from ..methods.base import TelegramMethod
from .defaults import BotDefaults
from .methods import BotMethods
from .session import AsyncSession

T = TypeVar("T")

logger = logging.getLogger(__name__)

_TOKEN = re.compile(r"\d+:[A-Za-z0-9_-]+")

_adapters: dict[Any, TypeAdapter[Any]] = {}


def _adapter(returning: Any) -> TypeAdapter[Any]:
    try:
        adapter = _adapters.get(returning)
    except TypeError:  # тип нельзя хешировать — строим без кеша
        return TypeAdapter(returning)

    if adapter is None:
        adapter = _adapters[returning] = TypeAdapter(returning)

    return adapter


class Bot(BotMethods):
    """Методы Bot API (send_message, get_me, ...) приходят из BotMethods."""

    session: AsyncSession
    token: str

    # Настройки транспорта: подкласс Bot переопределяет их атрибутом класса,
    # потому что диспетчер создаёт бота сам (bot = MyBot).
    request_timeout: float = 60.0  # на весь запрос; у getUpdates плюс его timeout
    connect_timeout: float = 10.0  # на установку соединения: мёртвая сеть падает быстро
    # 429: Telegram не выполнил запрос, поэтому подождать retry_after и повторить
    # безопасно. Ждём не дольше flood_max_wait секунд, иначе ошибка уходит в код.
    # flood_retries = 0 — не повторять вообще.
    flood_retries: int = 3
    flood_max_wait: float = 30.0
    # Значения по умолчанию для аргументов методов (parse_mode, link_preview_options, ...)
    defaults: BotDefaults = BotDefaults()
    # Прокси для запросов к Telegram ("http://host:port"); None — напрямую.
    proxy: str | None = None

    def __init__(
        self,
        token: str | None = None,
    ):

        # Токен: аргумент, а если его нет вообще (None) — старый путь, файл
        # bot_cfg.cfg в текущей папке (создаётся с заглушкой при первом запуске).
        # Файл трогаем только на этом пути: Bot("токен") ничего не пишет на диск.
        if token is None:
            token = ConfigAPI().get_token()

        if not token or not _TOKEN.fullmatch(token):
            raise ConfigError(
                "Нужен токен бота вида 123456:ABC-DEF: передайте Bot(token=...) "
                "или впишите bot_token в bot_cfg.cfg"
            )

        self.token = token
        self.session = AsyncSession(
            timeout=self.request_timeout,
            connect_timeout=self.connect_timeout,
            proxy=self.proxy,
        )
        self.username: str | None = None
        self.id = int(token.split(":")[0])

    async def call(self, method: TelegramMethod[T]) -> T:
        method = self.defaults.apply(method)

        retries = 0
        while True:
            response = await self.session(method=method, token=self.token)
            if response.get("ok"):
                break

            error = TelegramAPIError.from_response(method.__api_method__, response)
            if (
                isinstance(error, TelegramRetryAfter)
                and retries < self.flood_retries
                and error.retry_after <= self.flood_max_wait
            ):
                retries += 1
                logger.warning("%s: повтор через %s с (flood control)", error, error.retry_after)
                await asyncio.sleep(error.retry_after)
                continue

            raise error

        # context: объекты запоминают бота, поэтому message.answer() работает без ctx.
        return _adapter(method.__returning__).validate_python(
            response["result"], context={"bot": self}
        )

    async def download_file(self, file_path: str) -> bytes:
        """
        Байты файла по file_path (из get_file(file_id).file_path). Отдельный URL, не
        через call(): не JSON-ответ Bot API, лимит Telegram — 20 МБ на файл.
        """
        return await self.session.download(file_path, token=self.token)

    async def download(self, file_id: str) -> bytes:
        """get_file(file_id) и сразу download_file: байты файла по его id."""
        file = await self.get_file(file_id)
        if file.file_path is None:
            raise FileNotAvailableError(
                f"getFile({file_id!r}) не вернул file_path: файл недоступен для скачивания"
            )

        return await self.download_file(file.file_path)

    async def close_session(self) -> None:
        """Закрыть HTTP-сессию. (`close` — это метод Bot API, а не он.)"""
        await self.session.close()

    async def load_me(self) -> None:
        me = await self.get_me()
        self.username = me.username
