import logging
import os

from selfrot import BaseContext, BaseDispatcher, Bot, BotDefaults, MessageHandler
from selfrot.filter import Text
from selfrot.types import LinkPreviewOptions, TextMessage


class MyBot(Bot):
    # Как DefaultBotProperties(link_preview_is_disabled=True) у chestor_bot.
    defaults = BotDefaults(link_preview_options=LinkPreviewOptions(is_disabled=True))


class Ping(MessageHandler[BaseContext[TextMessage]]):
    query = Text("ping")

    async def handle(self) -> None:
        await self.ctx.answer_message("pong")


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = MyBot
    context = BaseContext
    handlers = (Ping,)

    async def on_startup(self) -> None:
        # Сюда идут фоновые воркеры приложения и разовая подготовка. Если бот раньше
        # работал вебхуком или поллингом, а теперь наоборот, старый режим надо снять:
        # пока вебхук установлен, getUpdates отвечает 409.
        if not os.environ.get("WEBHOOK_URL"):
            await self.api.delete_webhook(drop_pending_updates=True)

    async def on_shutdown(self) -> None:
        # Остановка воркеров и закрытие соединений; хендлеры к этому моменту закончили.
        ...


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    dp = Dispatcher(token=os.environ.get("BOT_TOKEN"))

    if url := os.environ.get("WEBHOOK_URL"):
        # Продакшен: https://example.org/webhook/<что-угодно> снаружи, nginx/Caddy
        # проксирует на этот порт. Секрет — в заголовке, а не в пути URL.
        dp.start_webhook(
            url=url,
            secret_token=os.environ["WEBHOOK_SECRET"],
            host="0.0.0.0",
            port=8999,
            drop_pending_updates=True,
        )
    else:
        dp.start_polling()
