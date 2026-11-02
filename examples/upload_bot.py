import logging
import os
from datetime import datetime
from pathlib import Path

from selfrot import BaseContext, BaseDispatcher, Bot, CommandArgs, MessageHandler, Rest
from selfrot.filter import Command
from selfrot.types import InputFile, InputMediaDocument, TextMessage

# Загрузка файлов, два способа.
#
#   /note <текст>  документ из байтов в памяти, аргументом метода — 1
#   /album         альбом: файлы из uploads/ рядом с ботом, плюс документ, на который
#                  ответили этой командой (он уже в Telegram — по file_id) — 2

UPLOADS = Path("uploads")
ALBUM_LIMIT = 10  # больше Telegram в один альбом не берёт


class NoteArgs(CommandArgs):
    text: Rest


# 1. Файл — аргумент метода: InputFile на месте document=. Байты из памяти или
# InputFile.from_path(...) с диска — разницы для вызова нет.
class Note(MessageHandler[BaseContext[TextMessage]]):
    """/note <текст> — пришлёт текст обратно файлом note.txt."""

    cmd = Command("note", NoteArgs)
    query = cmd

    async def handle(self) -> None:
        args = self.cmd.parse(self.ctx)
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        content = f"{stamp}\n\n{args.text}\n".encode()
        await self.ctx.reply_document(InputFile(content, "note.txt"), caption="Ваша заметка")


# 2. Файл — поле объекта: InputMediaDocument(media=InputFile(...)). В Bot API для этого
# есть «attach://<имя>» и отдельные части multipart; имена и части библиотека заводит
# сама, а file_id рядом остаётся обычной строкой. Файлы с диска уходят в сеть частями,
# целиком в память не читаются.
class Album(MessageHandler[BaseContext[TextMessage]]):
    """/album — файлы из uploads/ одним альбомом (и документ, на который ответили)."""

    query = Command("album")

    async def handle(self) -> None:
        media: list[InputMediaDocument] = []

        replied = self.ctx.message.reply_to_message
        if replied is not None and replied.document is not None:
            media.append(InputMediaDocument(media=replied.document.file_id))

        files = sorted(p for p in UPLOADS.glob("*") if p.is_file()) if UPLOADS.is_dir() else []
        for path in files[: ALBUM_LIMIT - len(media)]:
            media.append(InputMediaDocument(media=InputFile.from_path(path)))

        if len(media) < 2:  # альбом — от двух файлов
            await self.ctx.reply_message(
                f"Положите в {UPLOADS}/ хотя бы два файла (или один и ответьте /album "
                "на документ)."
            )
            return

        # Подпись альбома — подпись его первого элемента.
        first = media[0].model_copy(update={"caption": f"Файлов: {len(media)}"})
        await self.ctx.reply_media_group([first, *media[1:]])


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Note, Album)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
