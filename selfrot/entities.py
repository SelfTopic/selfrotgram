from collections.abc import Iterable

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
