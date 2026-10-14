from typing import Any

from ..context import BaseContext
from ..entities import mentions
from ..types import Message
from .base import BaseFilter


class HasMention(BaseFilter[BaseContext[Any]]):
    """
    В тексте или подписи сообщения есть кликабельное имя без username — Telegram сам
    подставляет его (сущность text_mention), когда выбираешь человека без username из
    автокомплита. Ничего не гарантирует само по себе (совпадает и через text, и через
    caption — какое из двух, статически не сказать); нужен text — добавьте HasText()
    или Command(...), у него он и так обязателен:

        Command("warn") & HasMention()

    Сами упоминания с пользователями внутри — mentions(ctx.message) или ctx.mentions().
    """

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and bool(mentions(event))
