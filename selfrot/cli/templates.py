"""
Шаблоны проекта для `selfrot init`. Только то, что касается самой библиотеки: диспетчер,
контекст, бот, роутеры и пустые места под клавиатуры, мидлвари и фильтры. Сервисы, БД
и репозитории приложение придумывает само.
"""

ENV_EXAMPLE = """\
# Токен бота от @BotFather (обязательно). Настоящий файл .env в git не коммитьте.
BOT_TOKEN=

# Вебхук вместо поллинга (нужен публичный HTTPS-адрес), см. src/bot/__main__.py:
# WEBHOOK_URL=https://example.org/webhook/bot
# WEBHOOK_SECRET=
"""

MAIN = '''\
import logging
import os
import sys

from selfrot import BaseDispatcher
from selfrot.middleware import LoggingMiddleware

from .bot import AppBot
from .context import AppContext
from .routers import RootRouter


class Dispatcher(BaseDispatcher[AppContext]):
    """Точка входа: собирает бота, контекст, роутеры и мидлвари."""

    bot = AppBot
    context = AppContext
    routers = (RootRouter,)
    middlewares = (LoggingMiddleware,)  # время обработки каждого апдейта в логе

    async def on_startup(self) -> None:
        """Перед началом приёма апдейтов (токен уже проверен): воркеры, соединения."""

    async def on_shutdown(self) -> None:
        """После остановки, когда начатые хендлеры доработали: закрыть всё открытое."""

    # Ответ пользователю на ошибки приложения; остальное только в лог:
    # async def on_error(self, ctx: AppContext, exc: Exception) -> None:
    #     await super().on_error(ctx, exc)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    token = os.environ.get("BOT_TOKEN")
    if not token:
        sys.exit("Задайте переменную окружения BOT_TOKEN (см. .env.example)")

    dispatcher = Dispatcher(token=token)

    # Вебхук вместо поллинга (за nginx/Caddy с HTTPS):
    # dispatcher.start_webhook(
    #     url=os.environ["WEBHOOK_URL"],
    #     secret_token=os.environ["WEBHOOK_SECRET"],
    #     host="0.0.0.0",
    #     port=8080,
    # )
    dispatcher.start_polling()


if __name__ == "__main__":
    main()
'''

BOT = '''\
from selfrot import Bot

# from selfrot import BotDefaults
# from selfrot.types import LinkPreviewOptions


class AppBot(Bot):
    """
    Настройки бота. Диспетчер создаёт бота сам (bot = AppBot), поэтому параметры
    задаются атрибутами класса.
    """

    # Значения по умолчанию для всех сообщений бота:
    # defaults = BotDefaults(
    #     parse_mode="HTML",
    #     link_preview_options=LinkPreviewOptions(is_disabled=True),
    # )

    # proxy = "http://host:port"
    # request_timeout = 60.0
'''

CONTEXT = '''\
from dataclasses import dataclass

from selfrot import BaseContext, TEvent


@dataclass
class AppContext(BaseContext[TEvent]):
    """
    Контекст одного апдейта: ctx.message, ctx.user, ctx.answer_message(...), ctx.fsm.
    Свои зависимости добавляются полями ниже, а передаются в
    Dispatcher.create_context:

        # greeter: GreetingService

        def create_context(self, update):
            return self.context(update, self.api, self.greeter)
    """
'''

ROUTERS = '''\
from selfrot import BaseRouter

from ..context import AppContext
from .start import StartRouter


class RootRouter(BaseRouter[AppContext]):
    """
    Корневой роутер: сюда подключаются все остальные. Новый роутер: положить модуль
    рядом (routers/profile.py), импортировать и добавить в кортеж. Порядок важен:
    апдейт достаётся первому подошедшему хендлеру.
    """

    routers = (StartRouter,)
    # Вместо импортов можно перечислить модули с переменной router:
    # auto_connect = (".start",)
'''

START = """\
from selfrot import BaseRouter, MessageHandler
from selfrot.filter import Command
from selfrot.types import TextMessage

from ..context import AppContext


class Start(MessageHandler[AppContext[TextMessage]]):
    query = Command("start")  # фильтр гарантирует, что у сообщения есть текст

    async def handle(self) -> None:
        await self.ctx.message.answer("Привет! Я бот на selfrotgram.")


class StartRouter(BaseRouter[AppContext]):
    handlers = (Start,)
"""


def package_files() -> dict[str, str]:
    """Файлы пакета бота (пути относительно него)."""
    return {
        "__init__.py": "",
        "__main__.py": MAIN,
        "bot.py": BOT,
        "context.py": CONTEXT,
        "routers/__init__.py": ROUTERS,
        "routers/start.py": START,
        "keyboards/__init__.py": "",
        "middlewares/__init__.py": "",
        "filters/__init__.py": "",
    }
