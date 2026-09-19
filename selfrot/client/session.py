import json
from typing import Any

import aiohttp

from ..exceptions import TelegramNetworkError, TelegramTimeout
from ..methods.base import TelegramMethod
from ..types import InputFile
from .telegram import TELEGRAM_API


async def _multipart(payload: dict[str, Any]) -> aiohttp.FormData:
    form = aiohttp.FormData()
    for key, value in payload.items():
        if isinstance(value, InputFile):
            form.add_field(
                key,
                await value.read(),
                filename=value.filename,
                content_type=value.content_type,
            )
        elif isinstance(value, bool):
            form.add_field(key, "true" if value else "false")
        elif isinstance(value, (dict, list)):
            form.add_field(key, json.dumps(value, ensure_ascii=False))
        else:
            form.add_field(key, str(value))

    return form


class AsyncSession:
    """
    Транспорт. Сам ничего не повторяет: любая сетевая беда — TelegramNetworkError
    (или TelegramTimeout), любой ответ Telegram — словарь (разбирает Bot.call).
    """

    session: aiohttp.ClientSession | None

    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        *,
        timeout: float = 60.0,
        connect_timeout: float = 10.0,
        proxy: str | None = None,
    ):
        self.session = session
        self._owns_session = session is None
        self.timeout = timeout
        self.connect_timeout = connect_timeout
        self.proxy = proxy

    async def create_session(self) -> aiohttp.ClientSession:
        if self.session is None:
            self.session = aiohttp.ClientSession()

        return self.session

    async def close(self) -> None:
        """Закрывает только свою сессию; переданную снаружи закрывает владелец."""
        if self._owns_session and self.session is not None:
            await self.session.close()
            self.session = None

    def _total_timeout(
        self, method: TelegramMethod[Any], payload: dict[str, Any]
    ) -> float:
        # getUpdates с timeout=N висит на стороне Telegram до N секунд: ждать ответ
        # надо дольше, иначе каждый пустой long polling считался бы обрывом.
        if method.__api_method__ == "getUpdates":
            return self.timeout + payload.get("timeout", 0)

        return self.timeout

    async def __call__(self, method: TelegramMethod[Any], token: str) -> dict[str, Any]:
        session = await self.create_session()
        url = TELEGRAM_API.get_url(token=token, method=method)
        payload = method.to_payload()
        total = self._total_timeout(method, payload)
        timeout = aiohttp.ClientTimeout(total=total, sock_connect=self.connect_timeout)

        try:
            # Файлы — multipart, всё остальное — JSON (вложенные объекты без
            # ручного json.dumps на каждый аргумент).
            if any(isinstance(value, InputFile) for value in payload.values()):
                request = session.post(
                    url,
                    data=await _multipart(payload),
                    timeout=timeout,
                    proxy=self.proxy,
                )
            else:
                request = session.post(
                    url, json=payload, timeout=timeout, proxy=self.proxy
                )

            async with request as response:
                status = response.status
                body = await response.text()
        except TimeoutError:
            raise TelegramTimeout(
                method.__api_method__, f"нет ответа за {total:g} с"
            ) from None
        except aiohttp.ClientError as e:
            # from None и замена токена: в str(e) и в цепочке причин лежит URL с токеном.
            reason = f"{type(e).__name__}: {e}".replace(token, "<token>")
            if self.proxy:
                reason = reason.replace(self.proxy, "<proxy>")
            raise TelegramNetworkError(method.__api_method__, reason) from None

        try:
            data = json.loads(body)
        except ValueError:
            data = None

        if not isinstance(data, dict):
            # Прокси, VPN или сам Telegram отдали не JSON (502 с HTML и т. п.).
            return {
                "ok": False,
                "error_code": status,
                "description": f"не JSON в ответе: {body[:200]!r}",
            }

        return data
