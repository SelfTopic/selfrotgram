from selfrot import BaseContext, Bot, entity_text, mentions
from selfrot.filter import HasMention
from selfrot.types import MessageEntity, User

from .conftest import TOKEN, bind, callback_update, message_update

MENTIONED = {"id": 42, "is_bot": False, "first_name": "Вася"}


def entity(offset: int, length: int, type_: str = "text_mention", **extra) -> MessageEntity:
    return MessageEntity(type=type_, offset=offset, length=length, **extra)


def ctx(raw: dict) -> BaseContext:
    api = Bot(TOKEN)
    return BaseContext(bind(raw, api), api)


class TestEntityText:
    def test_ascii(self):
        assert entity_text("забань Вася, пожалуйста", entity(7, 5)) == "Вася,"

    def test_emoji_before_entity_shifts_by_utf16_units_not_codepoints(self):
        # "😀" — суррогатная пара, 2 UTF-16 code unit, но 1 символ Python: индекс
        # Telegram и len()/срез Python не совпадают после такого символа.
        text = "привет 😀 Вася, бот"
        offset = len("привет 😀 ".encode("utf-16-le")) // 2
        assert entity_text(text, entity(offset, len("Вася"))) == "Вася"
        # Если бы считали в кодовых точках Python (без эмодзи как двух юнитов):
        assert text[offset : offset + len("Вася")] != "Вася"


class TestMentions:
    def test_text_mention_in_text(self):
        text = "привет, Вася!"
        offset, length = len("привет, "), len("Вася")
        message = message_update(
            text, entities=[entity(offset, length, user=MENTIONED).model_dump()]
        )
        result = mentions(bind(message, None).message)
        assert result == [("Вася", User(**MENTIONED))]

    def test_text_mention_in_caption(self):
        caption = "фото Вася"
        offset, length = len("фото "), len("Вася")
        message = message_update(
            None,
            photo=[{"file_id": "a", "file_unique_id": "b", "width": 1, "height": 1}],
            caption=caption,
            caption_entities=[entity(offset, length, user=MENTIONED).model_dump()],
        )
        result = mentions(bind(message, None).message)
        assert result == [("Вася", User(**MENTIONED))]

    def test_ignores_other_entity_types(self):
        text = "@username и обычный **bold**"
        message = message_update(
            text,
            entities=[
                entity(0, len("@username"), type_="mention").model_dump(),
                entity(len("@username и обычный "), 4, type_="bold").model_dump(),
            ],
        )
        assert mentions(bind(message, None).message) == []

    def test_no_entities(self):
        message = message_update("просто текст")
        assert mentions(bind(message, None).message) == []

    def test_no_text_or_caption(self):
        message = message_update(None)
        assert mentions(bind(message, None).message) == []

    def test_several_mentions_in_order(self):
        second = {"id": 7, "is_bot": False, "first_name": "Петя"}
        text = "Вася и Петя"
        message = message_update(
            text,
            entities=[
                entity(0, len("Вася"), user=MENTIONED).model_dump(),
                entity(len("Вася и "), len("Петя"), user=second).model_dump(),
            ],
        )
        result = mentions(bind(message, None).message)
        assert result == [("Вася", User(**MENTIONED)), ("Петя", User(**second))]


class TestContextMentions:
    def test_message_update(self):
        text = "Вася, прекрати"
        update = message_update(
            text, entities=[entity(0, len("Вася"), user=MENTIONED).model_dump()]
        )
        [(name, user)] = ctx(update).mentions()
        assert (name, user.id) == ("Вася", MENTIONED["id"])

    def test_callback_query_with_message_under_button(self):
        raw = callback_update("x")
        raw["callback_query"]["message"]["text"] = "Вася, тише"
        raw["callback_query"]["message"]["entities"] = [
            entity(0, len("Вася"), user=MENTIONED).model_dump()
        ]
        [(name, user)] = ctx(raw).mentions()
        assert (name, user.id) == ("Вася", MENTIONED["id"])

    def test_no_message_in_update(self):
        raw = {
            "update_id": 1,
            "inline_query": {
                "id": "1",
                "from": {"id": 7, "is_bot": False, "first_name": "u"},
                "query": "q",
                "offset": "",
            },
        }
        assert ctx(raw).mentions() == []


class TestHasMention:
    async def test_matches_message_with_mention(self):
        message = message_update(
            "Вася, прекрати", entities=[entity(0, len("Вася"), user=MENTIONED).model_dump()]
        )
        assert await HasMention().check(ctx(message)) is True

    async def test_does_not_match_without_mention(self):
        assert await HasMention().check(ctx(message_update("просто текст"))) is False

    async def test_does_not_match_other_entity_types(self):
        message = message_update(
            "@username тут", entities=[entity(0, len("@username"), type_="mention").model_dump()]
        )
        assert await HasMention().check(ctx(message)) is False

    async def test_does_not_match_non_message_event(self):
        raw = callback_update("x")  # callback_query — не Message
        assert await HasMention().check(ctx(raw)) is False
