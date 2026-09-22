import logging
import os
from collections import Counter

from selfrot import BaseContext, BaseDispatcher, Bot, MessageHandler
from selfrot.filter import (
    Command,
    HasReplyAnimation,
    HasReplyAudio,
    HasReplyCaption,
    HasReplyCaptionEntities,
    HasReplyDocument,
    HasReplyEntities,
    HasReplyPhoto,
    HasReplySticker,
    HasReplyText,
    HasReplyUser,
    HasReplyVideo,
    HasReplyVideoNote,
    HasReplyVoice,
)
from selfrot.middleware import LoggingMiddleware
from selfrot.types import (
    CaptionMessage,
    MessageEntity,
    PhotoMessage,
    Reply,
    ReplyCaptionEntitiesMessage,
    ReplyDocumentMessage,
    ReplyEntitiesMessage,
    ReplyStickerMessage,
    ReplyTextMessage,
    ReplyToMessageMessage,
    ReplyUserMessage,
    TextMessage,
    UserMessage,
)

# Ответ на сообщение: что известно про то, на что ответили. Запустите бота и отвечайте
# командами на разные сообщения (в личке или в группе, в группе бот отвечает на саму команду).
#
#   /warn причина  на сообщение человека          предупредить автора
#   /text          на текстовое сообщение          посчитать буквы и слова
#   /entities      на текст или подпись с форматом  что в нём: жирный, ссылки, упоминания
#   /sticker       на стикер                       эмодзи и набор
#   /file          на документ                     имя, тип и размер
#   /photo         на фото                         размер и автор
#   /caption       на фото с подписью              что подписано
#   /duration      на голосовое, аудио, видео...   сколько длится
#   /who           на что угодно                   кто автор
#   /help          где угодно                      это же в чате
#
# Три способа сузить тип, от простого к сложному (номера ниже): готовое условие,
# несколько условий сразу и обычный if.

HELP = """Команды работают в ответ на сообщение:
/warn причина: на сообщение человека
/text: на текст
/entities: на текст или подпись с форматированием
/sticker: на стикер
/file: на документ
/photo: на фото
/caption: на фото с подписью
/duration: на голосовое, аудио, видео, кружок или гифку
/who: на любое сообщение"""


# --- 1. Готовое условие -------------------------------------------------------------
# Тип в заголовке обещает («есть ответ, и у него известен автор»), фильтр проверяет, а ни
# assert, ни if не нужны. Гарантии разных полей складываются наследованием: text от
# TextMessage, ответ от ReplyUserMessage.
class WarnMessage(TextMessage, ReplyUserMessage, frozen=True): ...


class Warn(MessageHandler[BaseContext[WarnMessage]]):
    cmd = Command("warn")
    query = cmd & HasReplyUser()

    async def handle(self) -> None:
        offender = self.ctx.message.reply_to_message.user  # User, а не User | None
        if offender.is_bot:
            await self.ctx.message.reply("Ботов не предупреждаем.")
            return

        reason = self.cmd.call(self.ctx).rest or "без причины"
        await self.ctx.message.reply(
            f"Предупреждение: {offender.first_name} (id {offender.id}), {reason}"
        )


class TextCommand(TextMessage, ReplyTextMessage, frozen=True): ...


class TextStats(MessageHandler[BaseContext[TextCommand]]):
    query = Command("text") & HasReplyText()

    async def handle(self) -> None:
        text = self.ctx.message.reply_to_message.text  # str: у ответа точно есть текст
        await self.ctx.message.reply(
            f"Символов: {len(text)}, слов: {len(text.split())}."
        )


def describe(entities: list[MessageEntity]) -> str:
    kinds = Counter(entity.type for entity in entities)
    return ", ".join(f"{kind}: {count}" for kind, count in kinds.most_common())


class EntitiesCommand(TextMessage, ReplyEntitiesMessage, frozen=True): ...


class Entities(MessageHandler[BaseContext[EntitiesCommand]]):
    query = Command("entities") & HasReplyEntities()

    async def handle(self) -> None:
        entities = self.ctx.message.reply_to_message.entities  # list, а не None
        await self.ctx.message.reply(f"В тексте: {describe(entities)}.")


# У подписи к медиа свои сущности: это отдельное поле, поэтому отдельные тип и фильтр.
class CaptionEntitiesCommand(TextMessage, ReplyCaptionEntitiesMessage, frozen=True): ...


class CaptionEntities(MessageHandler[BaseContext[CaptionEntitiesCommand]]):
    query = Command("entities") & HasReplyCaptionEntities()

    async def handle(self) -> None:
        entities = self.ctx.message.reply_to_message.caption_entities
        await self.ctx.message.reply(f"В подписи: {describe(entities)}.")


class StickerCommand(TextMessage, ReplyStickerMessage, frozen=True): ...


class StickerInfo(MessageHandler[BaseContext[StickerCommand]]):
    query = Command("sticker") & HasReplySticker()

    async def handle(self) -> None:
        sticker = self.ctx.message.reply_to_message.sticker  # Sticker
        # Эмодзи и набор у стикера необязательные: тут обычный or, как для любого Optional.
        await self.ctx.message.reply(
            f"Стикер {sticker.emoji or '?'} из набора {sticker.set_name or 'без имени'}."
        )


class FileCommand(TextMessage, ReplyDocumentMessage, frozen=True): ...


class FileInfo(MessageHandler[BaseContext[FileCommand]]):
    query = Command("file") & HasReplyDocument()

    async def handle(self) -> None:
        document = self.ctx.message.reply_to_message.document  # Document
        size = f"{document.file_size / 1024:.1f} КБ" if document.file_size else "?"
        await self.ctx.message.reply(
            f"Файл {document.file_name or 'без имени'}, {document.mime_type or '?'}, {size}."
        )


# --- 2. Несколько условий над одним ответом -----------------------------------------
# «Фото и его автор». Фильтры складываются, как всегда: HasReplyPhoto() & HasReplyUser().
# А тип складывается на один уровень глубже: сначала собирают тип самого ответа (тем же
# наследованием, что на верхнем уровне), потом кладут его в Reply[...].
class PhotoAuthor(PhotoMessage, UserMessage, frozen=True): ...


class PhotoCommand(TextMessage, Reply[PhotoAuthor], frozen=True): ...


class PhotoInfo(MessageHandler[BaseContext[PhotoCommand]]):
    query = Command("photo") & HasReplyPhoto() & HasReplyUser()

    async def handle(self) -> None:
        photo = self.ctx.message.reply_to_message  # PhotoAuthor: и photo, и user на месте
        biggest = max(photo.photo, key=lambda size: size.width * size.height)
        await self.ctx.message.reply(
            f"Фото {biggest.width}x{biggest.height} от {photo.user.first_name}."
        )


# «Фото и с подписью».
class PhotoCaption(PhotoMessage, CaptionMessage, frozen=True): ...


class CaptionCommand(TextMessage, Reply[PhotoCaption], frozen=True): ...


class CaptionInfo(MessageHandler[BaseContext[CaptionCommand]]):
    query = Command("caption") & HasReplyPhoto() & HasReplyCaption()

    async def handle(self) -> None:
        photo = self.ctx.message.reply_to_message  # PhotoCaption
        await self.ctx.message.reply(
            f"Подпись: {photo.caption}. Размеров фото: {len(photo.photo)}."
        )


# --- 3. «Любое из» и обычный if -----------------------------------------------------
# Голосовое, аудио, видео, кружок или гифка: у всех есть duration, но это разные поля. Фильтр
# через | гарантирует лишь то, что верно для любой ветки, то есть просто «есть ответ». Какое
# именно поле заполнено, скажет обычная проверка в хендлере.
class DurationMessage(TextMessage, ReplyToMessageMessage, frozen=True): ...


class DurationInfo(MessageHandler[BaseContext[DurationMessage]]):
    query = Command("duration") & (
        HasReplyVoice()
        | HasReplyAudio()
        | HasReplyVideo()
        | HasReplyVideoNote()
        | HasReplyAnimation()
    )

    async def handle(self) -> None:
        reply = self.ctx.message.reply_to_message  # Message
        media = (
            reply.voice
            or reply.audio
            or reply.video
            or reply.video_note
            or reply.animation
        )
        if media is None:  # фильтр это исключает, а тип этого не знает
            return

        await self.ctx.message.reply(f"Длится {media.duration} с.")


# Условие редкое или своё: обычный if в хендлере, редактор сужает тип сам. Свой Reply[...] и
# свой фильтр стоит делать, только если то же условие нужно во многих хендлерах.
class Who(MessageHandler[BaseContext[TextMessage]]):
    query = Command("who")

    async def handle(self) -> None:
        reply = self.ctx.message.reply_to_message
        if reply is None:
            await self.ctx.message.reply("Ответьте командой на чьё-нибудь сообщение.")
            return

        if reply.user:
            await self.ctx.message.reply(
                f"Это {reply.user.first_name} (id {reply.user.id})."
            )
        else:
            await self.ctx.message.reply(
                "Автор неизвестен (сообщение из канала или анонимное)."
            )


# --- 4. Порядок и подсказки ---------------------------------------------------------
# Диспетчер идёт по хендлерам сверху вниз, и апдейт достаётся первому, чей фильтр пропустил.
# Значит, если команда дошла до этого хендлера, ни один хендлер выше её не взял: ответили
# не на то сообщение (или не ответили вовсе). Отдельные проверки в каждом хендлере для этого
# не нужны. Это то, что `if` внутри хендлера дать не может: там апдейт уже принят.
class Hint(MessageHandler[BaseContext[TextMessage]]):
    query = (
        Command("warn")
        | Command("text")
        | Command("entities")
        | Command("sticker")
        | Command("file")
        | Command("photo")
        | Command("caption")
        | Command("duration")
    )

    async def handle(self) -> None:
        await self.ctx.message.reply("Не то сообщение для этой команды.\n\n" + HELP)


class Help(MessageHandler[BaseContext[TextMessage]]):
    query = Command("help") | Command("start")

    async def handle(self) -> None:
        await self.ctx.message.reply(HELP)


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    # Порядок важен: Hint должен стоять после всех команд, которым нужен ответ.
    handlers = (
        Warn,
        TextStats,
        Entities,
        CaptionEntities,
        StickerInfo,
        FileInfo,
        PhotoInfo,
        CaptionInfo,
        DurationInfo,
        Who,
        Hint,
        Help,
    )
    middlewares = (LoggingMiddleware,)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
