import asyncio
import logging
import os
from pathlib import Path

from selfrot import BaseContext, BaseDispatcher, Bot, CommandArgs, MessageHandler, Rest
from selfrot.exceptions import ContextError, TelegramAPIError
from selfrot.filter import Command
from selfrot.types import TextMessage

# Скачивание файлов, два способа.
#
#   /save [имя]  в ответ на фото, документ, голосовое, видео, стикер... — 1
#   /resave <id> file_id без апдейта (например, сохранённый где-то раньше) — 2
#
# Файлы падают в downloads/ рядом с ботом.

DOWNLOADS = Path("downloads")


class SaveArgs(CommandArgs):
    name: Rest = ""  # необязательное: "/save отпуск" вместо безымянного "/save"


# 1. ctx.download сам находит файл в текущем апдейте: у фото берёт самый большой
# размер, иначе то, что заполнено (документ, голосовое, стикер, видео, ...). Пишет
# на диск и возвращает путь.
class Save(MessageHandler[BaseContext[TextMessage]]):
    """/save (на файле или в ответ на него), необязательно со своим именем."""

    cmd = Command("save", SaveArgs)
    query = cmd

    async def handle(self) -> None:
        args = self.cmd.parse(self.ctx)
        DOWNLOADS.mkdir(exist_ok=True)

        if args.name:
            # Своё имя могут дать двум разным файлам: overwrite=False не даст одному
            # затереть другой, допишет " (1)", " (2)", ...
            destination, overwrite = DOWNLOADS / args.name, False
        else:
            # message_id уникален всегда: коллизий не бывает, перезаписывать нечего.
            destination, overwrite = DOWNLOADS / str(self.ctx.message.message_id), True

        # Без расширения: ctx.download сам допишет то, что вернул Telegram (.jpg, .oga, ...).
        try:
            path = await self.ctx.download(destination, overwrite=overwrite)
        except ContextError:
            await self.ctx.message.reply(
                "Пришлите файл этой командой или ответьте ею на чьё-то сообщение с файлом."
            )
            return

        size = path.stat().st_size
        await self.ctx.message.reply(f"Сохранил {size} байт в {path}.")


class ResaveArgs(CommandArgs):
    file_id: str


# 2. Файл без апдейта, по одному id — например, сохранённому в базе после первого /save.
# bot.download(file_id) отдал бы сразу байты (и подошёл бы, если расширение не нужно), но
# только file_path из get_file знает настоящее расширение, поэтому здесь он вызван отдельно —
# то же самое, что делает bot.download внутри себя, только напоказ.
class Resave(MessageHandler[BaseContext[TextMessage]]):
    """/resave <file_id> — скачивает заново по id, безо всякого апдейта."""

    cmd = Command("resave", ResaveArgs)
    query = cmd

    async def handle(self) -> None:
        args = self.cmd.parse(self.ctx)

        try:
            file = await self.ctx.bot.get_file(args.file_id)
        except TelegramAPIError:
            await self.ctx.message.reply("Такой file_id скачать не получилось.")
            return

        if file.file_path is None:
            await self.ctx.message.reply("Такой file_id скачать не получилось.")
            return

        data = await self.ctx.bot.download_file(file.file_path)
        DOWNLOADS.mkdir(exist_ok=True)
        suffix = Path(file.file_path).suffix
        path = DOWNLOADS / f"resaved-{self.ctx.message.message_id}{suffix}"
        await asyncio.to_thread(path.write_bytes, data)
        await self.ctx.message.reply(f"Сохранил {len(data)} байт в {path}.")


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Save, Resave)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
