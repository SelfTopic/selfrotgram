from typing import Any

from ..context import BaseContext
from ..types import Message, TextMessage
from .strings import Contains, Endswith, Equals, Regexp, Startswith, StringFilter


class TextSource(StringFilter):
    """Текст сообщения (message.text). Гарантирует TextMessage."""

    guarantees = TextMessage

    def _read(self, ctx: BaseContext[Any]) -> str | None:
        event = ctx.event
        return event.text if isinstance(event, Message) else None


class Text(Equals, TextSource):
    """Текст равен образцу: Text("бот", ignore_case=True)."""


class TextStartswith(Startswith, TextSource):
    """Текст начинается с образца."""


class TextEndswith(Endswith, TextSource):
    """Текст заканчивается образцом."""


class TextContains(Contains, TextSource):
    """Текст содержит образец."""


class TextRegexp(Regexp, TextSource):
    """
    Текст подходит под выражение; match(ctx) отдаёт совпадение:

        pattern = TextRegexp(r"мут (\\d+)")
        query = pattern
        async def pre_handle(self): self.minutes = int(self.pattern.match(self.ctx)[1])
    """
