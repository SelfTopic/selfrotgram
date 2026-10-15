from dataclasses import dataclass
from typing import Any


class SelfrotError(Exception):
    """Корень всех ошибок библиотеки: `except SelfrotError` ловит любую."""


class ConfigError(SelfrotError):
    """Не хватает настройки (например, токена бота)."""


class DefinitionError(SelfrotError, TypeError):
    """
    Неверное описание хендлера, фильтра или роутера. Бросается при создании
    класса, то есть при импорте, а не в момент апдейта.
    """


class RouterError(SelfrotError, RuntimeError):
    """Дерево роутеров собрать нельзя: цикл, неверный путь auto_connect."""


class ContextError(SelfrotError, RuntimeError):
    """
    Действие не подходит апдейту: в нём нет чата, сообщения или объекта, из
    которого контекст берёт данные для ярлыка (ctx.answer_message, ...).
    """


class CallbackDataError(SelfrotError, ValueError):
    """
    Данные кнопки не упаковать или не разобрать: длиннее 64 байт (лимит Telegram),
    разделитель внутри значения, чужой префикс, значение не того типа.
    """


class KeyboardError(SelfrotError, ValueError):
    """Клавиатуру собрать нельзя: пустой или слишком широкий ряд, больше 100 кнопок."""


@dataclass(frozen=True)
class ArgProblem:
    """Что не так с одним аргументом команды."""

    field: str  # имя поля модели; пусто у проблем всей строки (лишние аргументы)
    message: str
    value: Any = None


class CommandArgsError(SelfrotError, ValueError):
    """
    Аргументы команды не подошли под модель CommandArgs: не то число, не тот тип,
    значение вне Literal. Хендлер получает её из parse() и ловит в on_error:

        problems — что именно не так (по полям), usage — «/calc <one> <operator> <two>»,
        command — имя команды, text — что написал пользователь.
    """

    def __init__(
        self, command: str, usage: str, problems: tuple[ArgProblem, ...], text: str
    ) -> None:
        found = "; ".join(f"{p.field}: {p.message}" if p.field else p.message for p in problems)
        super().__init__(f"{command}: неверные аргументы ({found}); ожидается: {usage}")
        self.command = command
        self.usage = usage
        self.problems = problems
        self.text = text


class DeferredLimitError(SelfrotError, RuntimeError):
    """
    Слишком много отложенных вызовов одновременно (Dispatcher.max_deferred). Из
    defer() приходит в on_error хендлера: можно ответить «попробуйте позже».
    """


class FSMError(SelfrotError, RuntimeError):
    """
    Состояние диалога не удалось прочитать или записать: неподходящее состояние,
    данные не той модели, у апдейта нет ключа.
    """


class BotNotBoundError(SelfrotError, RuntimeError):
    """
    Метод на объекте (message.answer, callback.answer) вызван у объекта, который не
    привязан к боту: создан вручную или разобран без контекста {"bot": ...}.
    """


class FileNotAvailableError(SelfrotError, RuntimeError):
    """
    getFile не вернул file_path, хотя в Bot API это поле формально Optional и на
    больших файлах, недоступных боту (например, старше 20 МБ), тоже. Скачать нечего.
    """


class FilterMatchError(SelfrotError, LookupError):
    """Разбор результата фильтра (match, parse) вызван без успешного check()."""


class TelegramNetworkError(SelfrotError):
    """
    До Telegram не достучались или не дождались ответа (обрыв, DNS, VPN). Запрос мог
    как дойти, так и не дойти: повторять отправку вслепую опасно, а вот getUpdates
    повторять можно. В тексте нет токена (aiohttp кладёт URL в свои ошибки).
    """

    def __init__(self, method: str, reason: str) -> None:
        super().__init__(f"{method}: {reason}")
        self.method = method
        self.reason = reason


class TelegramTimeout(TelegramNetworkError):
    """Telegram не ответил за отведённое время."""


class TelegramAPIError(SelfrotError):
    def __init__(
        self,
        method: str,
        error_code: int,
        description: str,
        parameters: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(f"{method}: [{error_code}] {description}")
        self.method = method
        self.error_code = error_code
        self.description = description
        self.parameters = parameters or {}

    @classmethod
    def from_response(cls, method: str, response: dict[str, Any]) -> "TelegramAPIError":
        code = int(response.get("error_code", 0))
        description = response.get("description", "")
        error_type: type[TelegramAPIError] = TelegramAPIError

        if code == 400:
            error_type = _bad_request_subtype(description)
        elif code == 401:
            error_type = TelegramUnauthorized
        elif code == 403:
            error_type = TelegramForbidden
        elif code == 404:
            error_type = TelegramNotFound
        elif code == 409:
            error_type = TelegramConflict
        elif code == 429:
            error_type = TelegramRetryAfter
        elif code >= 500:
            error_type = TelegramServerError

        return error_type(method, code, description, response.get("parameters"))


class TelegramBadRequest(TelegramAPIError): ...


class MessageNotModified(TelegramBadRequest):
    """
    Новое содержимое (текст и/или клавиатура) совпадает с уже отправленным — Telegram
    не считает это правкой и отказывает. Обычно безопасно игнорировать: сообщение и так
    уже выглядит так, как нужно.
    """


class MessageToEditNotFound(TelegramBadRequest):
    """
    Сообщение, которое правите или удаляете, уже недоступно (удалено пользователем,
    слишком старое, или это не сообщение бота). Обычно безопасно игнорировать: цели
    (убрать клавиатуру, поправить текст) уже некуда применять.
    """


# (искать в description, тип) — первое совпадение побеждает; description у Telegram
# всегда начинается с "Bad Request: ", но ищем без привязки к точному префиксу/регистру.
_BAD_REQUEST_SUBTYPES: tuple[tuple[str, type[TelegramBadRequest]], ...] = (
    ("message is not modified", MessageNotModified),
    ("message to edit not found", MessageToEditNotFound),
)


def _bad_request_subtype(description: str) -> type[TelegramBadRequest]:
    lowered = description.lower()
    for needle, subtype in _BAD_REQUEST_SUBTYPES:
        if needle in lowered:
            return subtype

    return TelegramBadRequest


class TelegramUnauthorized(TelegramAPIError): ...


class TelegramForbidden(TelegramAPIError): ...


class TelegramNotFound(TelegramAPIError): ...


class TelegramConflict(TelegramAPIError): ...


class TelegramServerError(TelegramAPIError): ...


class TelegramRetryAfter(TelegramAPIError):
    @property
    def retry_after(self) -> int:
        return int(self.parameters.get("retry_after", 0))
