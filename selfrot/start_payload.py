import re
from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar, Self, get_args

from pydantic import BaseModel, ValidationError

from .exceptions import DefinitionError, StartPayloadError

if TYPE_CHECKING:
    from .client import Bot

MAX_CHARS = 64  # лимит Telegram на параметр start= в deep link
# Единственный алфавит, который Telegram пропускает в t.me/<bot>?start=...; всё
# остальное молча режется при переходе по ссылке — не 400, просто пустой параметр.
_ALPHABET = re.compile(r"[A-Za-z0-9_-]+")


def _encode(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, Enum):
        return str(value.value)

    return str(value)


class StartPayload(BaseModel):
    """
    Типизированные данные deep link (t.me/<bot>?start=...). У обычной кнопки в
    callback_data можно положить что угодно (Telegram разрешает любые байты до 64),
    а параметр start= — только [A-Za-z0-9_-], до 64 символов, иначе Telegram молча
    отбрасывает его при переходе по ссылке. Поэтому не вариант CallbackPayload, а
    отдельный класс со своей упаковкой (через sep, по умолчанию "_" — ":" в алфавит
    не входит):

        class MarryLink(StartPayload, prefix="marry"):
            proposal_id: int

        url = MarryLink(proposal_id=5).url(bot)   # t.me/<bot>?start=marry_5

    Разбор — не руками: Command("start", MarryLink, deep_link=True), тот же .parse(ctx),
    что и у обычных аргументов команды (см. filter/command.py).
    """

    __prefix__: ClassVar[str]
    __sep__: ClassVar[str]

    def __init_subclass__(cls, *, prefix: str, sep: str = "_", **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not prefix or not sep or sep in prefix:
            raise DefinitionError(
                f"{cls.__name__}: prefix не пустой и без разделителя {sep!r} внутри"
            )
        if not _ALPHABET.fullmatch(prefix) or not _ALPHABET.fullmatch(sep):
            raise DefinitionError(
                f"{cls.__name__}: prefix и sep — только [A-Za-z0-9_-] "
                "(единственный алфавит, который Telegram пропускает в ссылке)"
            )

        cls.__prefix__ = prefix
        cls.__sep__ = sep

    def pack(self) -> str:
        sep = self.__sep__
        parts = [self.__prefix__]
        for name in type(self).model_fields:
            text = _encode(getattr(self, name))
            if text and not _ALPHABET.fullmatch(text):
                raise StartPayloadError(
                    f"{type(self).__name__}.{name}={text!r}: вне алфавита "
                    "[A-Za-z0-9_-], Telegram такую ссылку молча испортит"
                )
            parts.append(text)

        data = sep.join(parts)
        if len(data) > MAX_CHARS:
            raise StartPayloadError(
                f"{type(self).__name__}: deep link {len(data)} символов, максимум "
                f"{MAX_CHARS} ({data!r})"
            )

        return data

    def url(self, bot: "Bot") -> str:
        """t.me/<username>?start=<pack()>. Нужен bot.username (грузится getMe() —
        к моменту, когда дошло до хендлера, диспетчер его уже загрузил)."""
        if bot.username is None:
            raise StartPayloadError(
                "bot.username ещё не известен: getMe() не вызывался "
                "(обычно его вызывает диспетчер перед стартом)"
            )

        return f"https://t.me/{bot.username}?start={self.pack()}"

    @classmethod
    def unpack(cls, data: str) -> Self:
        sep = cls.__sep__
        head, *rest = data.split(sep)
        fields = cls.model_fields
        if head != cls.__prefix__ or len(rest) != len(fields):
            raise StartPayloadError(f"{data!r} не подходит под {cls.__name__}")

        raw: dict[str, Any] = {}
        for (name, field), text in zip(fields.items(), rest, strict=True):
            optional = type(None) in get_args(field.annotation)
            raw[name] = None if text == "" and optional else text

        try:
            return cls.model_validate(raw)
        except ValidationError as e:
            raise StartPayloadError(f"{data!r}: {cls.__name__}: {e}") from e

    @classmethod
    def try_unpack(cls, data: str) -> Self | None:
        try:
            return cls.unpack(data)
        except StartPayloadError:
            return None
