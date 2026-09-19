import hmac
import logging
import re
from collections import OrderedDict
from collections.abc import Awaitable, Callable
from typing import Any

from aiohttp import web

from ..exceptions import ConfigError
from ..types import Update

logger = logging.getLogger(__name__)

SECRET_HEADER = "X-Telegram-Bot-Api-Secret-Token"
_SECRET_PATTERN = re.compile(r"[A-Za-z0-9_-]{1,256}")


def check_secret_token(secret_token: str) -> None:
    """Telegram принимает в secret_token только эти символы и не больше 256."""
    if not _SECRET_PATTERN.fullmatch(secret_token):
        raise ConfigError("secret_token: от 1 до 256 символов из A-Z, a-z, 0-9, _ и -")


class WebhookApp:
    """
    HTTP-приложение, которое принимает апдейты от Telegram.

    - без верного секрета в заголовке — 403 (иначе любой, кто знает URL, может
      прислать «апдейт от администратора»);
    - ответ 200 сразу после постановки апдейта в очередь, а не после обработки:
      если хендлер долгий, Telegram не сочтёт запрос проваленным и не пришлёт
      апдейт повторно;
    - очередь переполнена — 503: Telegram повторит позже (апдейт при этом не
      запоминается как принятый);
    - повторно присланный апдейт (Telegram повторяет при сбое или медленном ответе)
      отбрасывается по update_id.
    """

    def __init__(
        self,
        feed: Callable[[Update], Awaitable[bool]],
        path: str,
        secret_token: str,
        bot: Any = None,
        seen_limit: int = 1000,
    ) -> None:
        check_secret_token(secret_token)
        self._feed = feed
        self._bot = bot
        self._path = path
        self._secret = secret_token.encode()
        self._seen: OrderedDict[int, None] = OrderedDict()
        self._seen_limit = seen_limit

    def build(self) -> web.Application:
        app = web.Application()
        app.router.add_post(self._path, self._handle)
        return app

    def _remember(self, update_id: int) -> None:
        self._seen[update_id] = None
        while len(self._seen) > self._seen_limit:
            self._seen.popitem(last=False)

    async def _handle(self, request: web.Request) -> web.Response:
        given = request.headers.get(SECRET_HEADER, "").encode()
        if not hmac.compare_digest(given, self._secret):
            return web.Response(status=403)

        try:
            # context: объекты запоминают бота (message.answer() без ctx)
            update = Update.model_validate(
                await request.json(), context={"bot": self._bot}
            )
        except ValueError:  # плохой JSON и ValidationError pydantic
            return web.Response(status=400)

        if update.update_id in self._seen:
            logger.info("update %s уже принят, повтор отброшен", update.update_id)
            return web.Response()

        if not await self._feed(update):
            logger.warning(
                "update %s: очередь переполнена, ответ 503", update.update_id
            )
            return web.Response(status=503, headers={"Retry-After": "1"})

        self._remember(update.update_id)
        return web.Response()
