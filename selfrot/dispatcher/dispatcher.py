import asyncio
import logging
import signal
from collections.abc import AsyncGenerator, Awaitable, Hashable
from functools import partial
from typing import (
    Any,
    Generic,
)
from urllib.parse import urlparse

from aiohttp import web

from ..client import Bot
from ..context import TContext
from ..exceptions import SelfrotError, TelegramNotFound, TelegramUnauthorized
from ..fsm import FSM, MemoryStorage, Storage
from ..router import BaseRouter
from ..types import Update
from .runner import UpdateRunner
from .webhook import WebhookApp, check_secret_token

logger = logging.getLogger(__name__)


async def _until_signal(main: Awaitable[Any]) -> None:
    """
    Выполняет main до SIGINT/SIGTERM: сигнал отменяет задачу, а её `finally`
    (drain, on_shutdown, закрытие сессии) отрабатывает штатно. SIGTERM — это
    остановка контейнера (docker stop), без такой обработки процесс убивался бы
    посреди хендлеров.
    """
    task = asyncio.ensure_future(main)
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, task.cancel)
        except NotImplementedError:  # Windows
            pass

    try:
        await task
    except asyncio.CancelledError:
        if not task.cancelled():
            raise


class BaseDispatcher(BaseRouter[TContext], Generic[TContext]):

    # Класс бота; свои настройки (defaults, proxy, таймауты) — в подклассе Bot.
    bot: type[Bot] = Bot
    # Long polling: Telegram держит getUpdates до стольких секунд, пока не появится
    # апдейт. 0 — короткие запросы с паузой в секунду (только для отладки).
    polling_timeout: int = 30
    # Обработка параллельная: не больше стольких апдейтов одновременно (1 —
    # строго по очереди). Когда лимит выбран, новые апдейты не забираются.
    max_concurrent_updates: int = 100
    # При остановке начатым хендлерам даётся столько секунд, потом их отменяют.
    shutdown_timeout: float = 10.0
    # Хранилище состояний диалогов (ctx.fsm). None — MemoryStorage (пропадает при
    # перезапуске); своё: fsm_storage = MemoryStorage(ttl=600) или любой Storage.
    fsm_storage: Storage | None = None

    def __init__(self, token: str | None = None) -> None:
        """
        token — токен бота из настроек проекта: `Root(token=settings.BOT_TOKEN)`. Без
        него бот читает bot_token из bot_cfg.cfg в текущей папке.
        """
        super().__init__()
        self.api = self.bot(token)
        self._runner = UpdateRunner(self.max_concurrent_updates, self.shutdown_timeout)
        # Свой экземпляр на диспетчер: общий на уровне класса делили бы все диспетчеры.
        self._fsm_storage: Storage = self.fsm_storage or MemoryStorage()

    async def poll_updates(self) -> AsyncGenerator[Update, None]:

        # Без allowed_updates Telegram не присылает chat_member и реакции, а
        # остальное присылает лишнее. Берём ровно то, на что есть хендлеры.
        allowed_updates = sorted(self.used_update_types())

        offset = 0
        delay = 1.0
        while True:

            try:
                updates = await self.api.get_updates(
                    offset=offset,
                    timeout=self.polling_timeout,
                    allowed_updates=allowed_updates,
                )
            except TelegramUnauthorized:
                raise  # токен отозван — повторами не лечится
            except SelfrotError as e:
                # Обрыв сети, 5xx, 409 (второй экземпляр бота) и т. п.: ждём с
                # нарастающей паузой, а не долбим Telegram вхолостую.
                logger.warning("getUpdates: %s; повтор через %g с", e, delay)
                await asyncio.sleep(delay)
                delay = min(delay * 2, 30.0)
                continue

            delay = 1.0

            if updates:
                offset = updates[-1].update_id + 1
            elif self.polling_timeout == 0:
                await asyncio.sleep(1.0)

            for update in updates:
                yield update

    def create_context(self, update: Update) -> TContext:
        return self.context(update, self.api)

    async def _load_bot_info(self) -> None:
        # username нужен фильтрам вроде Command для /command@username.
        # Сетевые сбои ретраим, неверный токен (401/404) — нет.
        while True:
            try:
                await self.api.load_me()
                return
            except (TelegramUnauthorized, TelegramNotFound):
                raise
            except SelfrotError as e:
                logger.warning("getMe: %s; повтор через 1 с", e)
                await asyncio.sleep(1.0)

    def ordering_key(self, ctx: TContext) -> Hashable | None:
        """
        Апдейты с одинаковым ключом обрабатываются строго по очереди, с разными —
        параллельно. По умолчанию None: порядка нет, каждый апдейт независим (как в
        aiogram), поэтому долгий хендлер ничего не задерживает, а гонки за данные
        решает приложение. Порядок включается явно:

            def ordering_key(self, ctx):
                return order_by_chat(ctx)   # или order_by_user(ctx), или свой ключ
        """
        return None

    async def on_error(self, ctx: TContext, exc: Exception) -> None:
        """
        Последняя инстанция: сюда доходит всё, что не обработал on_error хендлера
        (или хендлер не нашёлся: упала мидлварь диспетчера, фильтр). По умолчанию
        пишет в лог. Переопределяется: сообщить админу, ответить пользователю на
        свои исключения и т. п.
        """
        logger.error(
            "Ошибка при обработке update %s", ctx.update.update_id, exc_info=exc
        )

    def fsm_key(self, ctx: TContext) -> str | None:
        """
        Чей это диалог. По умолчанию «чат:пользователь»: в группе у каждого участника
        свой сценарий, в личке чат совпадает с пользователем. Переопределяется:
        `return str(ctx.chat_id)` — один сценарий на весь чат. None — у апдейта нет
        ни чата, ни пользователя (состояние некуда привязать).
        """
        chat, user = ctx.chat, ctx.user
        if user is None:
            return None

        return f"{chat.id if chat else user.id}:{user.id}"

    async def _handle(self, ctx: TContext) -> None:
        if ctx._fsm is None:
            ctx._fsm = FSM(self._fsm_storage, self.fsm_key(ctx))

        # Ошибка одного апдейта (в том числе сеть при ответе, и даже сам on_error)
        # не должна ронять бота.
        try:
            try:
                await self.propagate(ctx)
            except Exception as exc:  # noqa: BLE001 - граница: дальше своя обработка
                await self.on_error(ctx, exc)
        except Exception:
            logger.exception("on_error упал на update %s", ctx.update.update_id)

    async def on_startup(self) -> None:
        """
        Перед началом приёма апдейтов (токен уже проверен через getMe): запустить
        фоновые воркеры, открыть соединения, при необходимости
        `await self.api.delete_webhook(drop_pending_updates=True)`. Переопределяется.
        """

    async def on_shutdown(self) -> None:
        """
        После остановки, когда начатые хендлеры уже закончили (или отменены):
        остановить воркеры, закрыть соединения. Вызывается, если on_startup был
        начат, даже если он упал посередине, поэтому останавливать нужно то, что
        могло и не запуститься. Переопределяется.
        """

    async def feed_update(self, update: Update) -> None:
        """
        Отдать апдейт на обработку (ждёт свободного слота). Так апдейты попадают
        из поллинга и вебхука; можно звать и из своего веб-приложения.
        """
        ctx = self.create_context(update)
        await self._runner.submit(self.ordering_key(ctx), partial(self._handle, ctx))

    async def try_feed_update(self, update: Update) -> bool:
        """Как feed_update, но без ожидания: False, если все слоты заняты."""
        ctx = self.create_context(update)
        return await self._runner.try_submit(
            self.ordering_key(ctx), partial(self._handle, ctx)
        )

    async def _stop(self, started: bool) -> None:
        logger.info("Остановка: дожидаюсь начатых хендлеров")
        try:
            await self._runner.drain()
            if started:
                await self.on_shutdown()
        finally:
            await self.api.close_session()

    async def polling(self) -> None:
        started = False
        try:
            await self._load_bot_info()

            started = True
            await self.on_startup()

            logger.info("Запущен @%s, жду апдейты (long polling)", self.api.username)
            async for update in self.poll_updates():
                await self.feed_update(update)
        finally:
            await self._stop(started)

    async def webhook(
        self,
        *,
        url: str,
        secret_token: str,
        host: str = "127.0.0.1",
        port: int = 8080,
        drop_pending_updates: bool = False,
        max_connections: int | None = None,
    ) -> None:
        """
        Принимать апдейты вебхуком. url — публичный HTTPS-адрес (Telegram шлёт только
        на HTTPS), путь из него становится путём сервера; TLS обычно терминирует
        nginx/Caddy перед ботом, а сервер слушает обычный HTTP на host:port
        (в контейнере нужен host="0.0.0.0"). secret_token обязателен. Сервер
        запускается раньше setWebhook, чтобы первые апдейты не упёрлись в закрытый порт.
        """
        check_secret_token(secret_token)
        path = urlparse(url).path or "/"
        site_runner: web.AppRunner | None = None
        started = False
        try:
            await self._load_bot_info()

            started = True
            await self.on_startup()

            app = WebhookApp(
                self.try_feed_update, path, secret_token, bot=self.api
            ).build()
            # access_log=None: в строке запроса лежит путь, а в нём может быть секрет.
            site_runner = web.AppRunner(app, access_log=None)
            await site_runner.setup()
            await web.TCPSite(site_runner, host=host, port=port).start()

            await self.api.set_webhook(
                url,
                secret_token=secret_token,
                allowed_updates=sorted(self.used_update_types()),
                drop_pending_updates=drop_pending_updates or None,
                max_connections=max_connections,
            )
            logger.info("Вебхук установлен: %s (сервер на %s:%s)", url, host, port)

            await asyncio.Event().wait()  # до отмены (сигнал остановки)
        finally:
            try:
                if site_runner is not None:
                    await site_runner.cleanup()  # перестаём принимать новые запросы
            finally:
                await self._stop(started)

    def start_polling(self) -> None:
        asyncio.run(_until_signal(self.polling()))

    def start_webhook(
        self,
        *,
        url: str,
        secret_token: str,
        host: str = "127.0.0.1",
        port: int = 8080,
        drop_pending_updates: bool = False,
        max_connections: int | None = None,
    ) -> None:
        asyncio.run(
            _until_signal(
                self.webhook(
                    url=url,
                    secret_token=secret_token,
                    host=host,
                    port=port,
                    drop_pending_updates=drop_pending_updates,
                    max_connections=max_connections,
                )
            )
        )
