import html
from collections.abc import Iterable
from typing import overload

from .exceptions import DefinitionError
from .types import Message, MessageEntity, User


def entity_text(text: str, entity: MessageEntity) -> str:
    """
    Текст сущности, вырезанный по offset/length. Telegram считает их в единицах
    UTF-16, а не в кодовых точках Python (`len(text)`) — без этого текст после любого
    символа за пределами BMP (эмодзи, некоторые редкие иероглифы: занимают два UTF-16
    code unit, суррогатную пару, но один символ Python) съезжает. `text` — то, откуда
    вырезаем (message.text, message.caption, TextQuote.text — у кого есть entities).

        offender_name = entity_text(message.text, entity)   # entity.type == "text_mention"
    """
    units = text.encode("utf-16-le")
    start = entity.offset * 2
    end = start + entity.length * 2
    return units[start:end].decode("utf-16-le")


def mentions(message: Message) -> list[tuple[str, User]]:
    """
    Упоминания без username — кликабельное имя, которое Telegram сам подставляет из
    списка участников (сущность text_mention, с пользователем внутри, не угадывается
    по тексту): (кликабельный текст, пользователь) для каждого. У сообщения заполнено
    либо text+entities, либо caption+caption_entities (никогда оба одновременно) —
    сама разбирается, какое. Нет текста или сущностей — [].

        for name, user in mentions(ctx.message):
            await warn(user, reason=f"упомянут как {name!r}")

    Сущности самого сообщения, не того, на которое оно отвечает: для ctx.message.
    reply_to_message позовите mentions(message.reply_to_message) явно.
    """
    text = message.text if message.text is not None else message.caption
    entities: Iterable[MessageEntity] | None = (
        message.entities if message.entities is not None else message.caption_entities
    )
    if text is None or not entities:
        return []

    return [
        (entity_text(text, entity), entity.user)
        for entity in entities
        if entity.type == "text_mention" and entity.user is not None
    ]


@overload
def mention_html(user: User, /) -> str: ...
@overload
def mention_html(telegram_id: int, name: str, /) -> str: ...
def mention_html(user: "User | int", name: str | None = None, /) -> str:
    """
    Кликабельное имя без username, в другую сторону от mentions(): не прочитать
    готовое, а собрать своё — то же самое, что Telegram сам вставляет в текст, когда
    у человека нет username ("tg://user?id=..."), чтобы вставить его text_mention'ом
    в сообщение с parse_mode="HTML".

        mention_html(user)                     # User из апдейта: имя сам из first_name/last_name
        mention_html(user.id, "Вася из базы")   # тикер/сервис держит только id и имя, не User

    Имя экранируется само (`&`, `<`, `>` — всё, что требует Telegram в HTML
    parse_mode): готовую строку из БД можно передавать как есть, не оборачивать
    каждый вызов в html.escape() руками.
    """
    if isinstance(user, User):
        telegram_id = user.id
        display = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
    else:
        if name is None:
            raise DefinitionError(
                "mention_html(telegram_id, name): без User нужно имя вторым параметром"
            )
        telegram_id = user
        display = name

    return f'<a href="tg://user?id={telegram_id}">{html.escape(display, quote=False)}</a>'
