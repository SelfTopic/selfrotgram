from dataclasses import dataclass
from typing import Any

from ..context import BaseContext
from ..exceptions import DefinitionError, FilterMatchError
from ..types import Message, TextMessage
from .base import BaseFilter


@dataclass(frozen=True)
class CommandCall:
    """Разбор сообщения с командой."""

    prefix: str
    args: tuple[str, ...]
    rest: str  # всё после команды как написано (без крайних пробелов)


class Command(BaseFilter[BaseContext[TextMessage]]):
    """
    /name аргумент аргумент. Имя может быть из нескольких слов, префикс — любым:

        Command("imut", prefixes="/!")           # /imut, !imut
        Command("бот скажи", prefixes="", ignore_case=True)

    prefixes — строка из односимвольных префиксов; "" — команда без префикса.
    Если задан args_count, число аргументов должно совпасть точно, иначе апдейт
    этому хендлеру не подходит.

    /name@username (только с префиксом "/") подходит, если username — этого бота
    (Bot.username загружает диспетчер при старте через getMe; пока он неизвестен,
    команды с упоминанием не совпадают).

    Аргументы в хендлере: parse(ctx) — явно, как match(ctx) у регулярных выражений.
    """

    guarantees = TextMessage

    def __init__(
        self,
        name: str,
        args_count: int | None = None,
        *,
        prefixes: str = "/",
        ignore_case: bool = False,
    ) -> None:
        self.words = tuple(name.split())
        if not self.words:
            raise DefinitionError("Command: пустое имя")
        if name.startswith(tuple(prefixes)):
            raise DefinitionError(f"Command({name!r}): имя пишется без префикса")

        self.name = name
        self.args_count = args_count
        self.prefixes = tuple(prefixes) or ("",)
        self.ignore_case = ignore_case

    def _fold(self, text: str) -> str:
        return text.casefold() if self.ignore_case else text

    def _parse(self, ctx: BaseContext[Any]) -> CommandCall | None:
        message = ctx.event
        if not isinstance(message, Message) or message.text is None:
            return None

        count = len(self.words)
        parts = message.text.split(None, count)
        if len(parts) < count:
            return None

        for prefix in self.prefixes:
            head = parts[0]
            if not head.startswith(prefix):
                continue

            head = head[len(prefix) :]
            if prefix == "/":
                head, _, mention = head.partition("@")
                if mention and not self._is_me(ctx, mention):
                    continue

            written = (head, *parts[1:count])
            if [self._fold(w) for w in written] != [self._fold(w) for w in self.words]:
                continue

            rest = parts[count].rstrip() if len(parts) > count else ""
            args = tuple(rest.split())
            if self.args_count is not None and len(args) != self.args_count:
                return None

            return CommandCall(prefix=prefix, args=args, rest=rest)

        return None

    @staticmethod
    def _is_me(ctx: BaseContext[Any], mention: str) -> bool:
        username = ctx.bot.username
        return username is not None and mention.lower() == username.lower()

    async def check(self, ctx: BaseContext[Any]) -> bool:
        return self._parse(ctx) is not None

    def parse(self, ctx: BaseContext[Any]) -> CommandCall:
        """Префикс и аргументы. Только после того, как check() сказал да."""
        call = self._parse(ctx)
        if call is None:
            raise FilterMatchError(f"{self!r} не подошёл к этому апдейту")

        return call

    def __repr__(self) -> str:
        return f"Command({self.name!r})"
