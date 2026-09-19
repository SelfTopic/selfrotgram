from typing import Any, Self

from .callback_data import MAX_BYTES, CallbackPayload
from .exceptions import CallbackDataError, KeyboardError
from .types import InlineKeyboardButton, InlineKeyboardMarkup

MAX_IN_ROW = 8  # лимиты Telegram
MAX_BUTTONS = 100
# По спеке ровно одно поле кроме этих задаёт вид кнопки.
_NOT_KIND = {"text", "icon_custom_emoji_id", "style"}


def button(
    text: str,
    data: str | CallbackPayload | None = None,
    *,
    url: str | None = None,
    **fields: Any,
) -> InlineKeyboardButton:
    """
    Кнопка. data — callback_data строкой или CallbackPayload; url — кнопка-ссылка;
    остальные поля InlineKeyboardButton — по имени (web_app=..., style="success"):

        button("Принять", Duel(duel_id=1, action="accept", expected_id=5))
        button("Сайт", url="https://example.org")

    Проверяется до отправки то, что иначе Telegram отвергнет ответом 400: ровно
    один вид кнопки, callback_data 1-64 байт, неизвестные поля (опечатки).
    """
    known = set(InlineKeyboardButton.model_fields)
    unknown = set(fields) - known
    if unknown:
        raise KeyboardError(
            f"button(): нет полей {sorted(unknown)} у InlineKeyboardButton"
        )

    if isinstance(data, CallbackPayload):
        callback_data: str | None = data.pack()
    else:
        callback_data = data
        if callback_data is not None:
            size = len(callback_data.encode())
            if not 1 <= size <= MAX_BYTES:
                raise CallbackDataError(
                    f"callback_data {size} байт, нужно от 1 до {MAX_BYTES} ({callback_data!r})"
                )

    given = {"callback_data": callback_data, "url": url, **fields}
    kinds = [
        name
        for name, value in given.items()
        if name not in _NOT_KIND and value is not None
    ]
    if len(kinds) != 1:
        raise KeyboardError(
            f"кнопка {text!r}: нужен ровно один вид (callback_data, url, web_app, ...), "
            f"задано: {kinds or 'ничего'}"
        )

    return InlineKeyboardButton(
        text=text, **{k: v for k, v in given.items() if v is not None}
    )


class InlineKeyboard:
    """
    Сборщик инлайн-клавиатуры. button() кладёт кнопки в ряды по width штук
    (одна на ряд по умолчанию), row() — отдельный ряд из перечисленных:

        kb = InlineKeyboard(width=2)
        for i, option in enumerate(options):
            kb.button(option, QuizAnswer(question_id=q.id, index=i))
        kb.row(button("Пропустить", "quiz_skip"))
        await msg.reply(q.text, reply_markup=kb.markup())

    Лимиты Telegram (8 кнопок в ряду, 100 всего) проверяются при добавлении.
    """

    def __init__(self, width: int = 1) -> None:
        if not 1 <= width <= MAX_IN_ROW:
            raise KeyboardError(f"width от 1 до {MAX_IN_ROW}, получено {width}")

        self.width = width
        self._rows: list[list[InlineKeyboardButton]] = []
        self._open = False  # последний ряд ещё принимает кнопки из button()
        self._count = 0

    def _check_room(self, extra: int) -> None:
        if self._count + extra > MAX_BUTTONS:
            raise KeyboardError(f"в клавиатуре не больше {MAX_BUTTONS} кнопок")

    def button(
        self,
        text: str,
        data: str | CallbackPayload | None = None,
        *,
        url: str | None = None,
        **fields: Any,
    ) -> Self:
        self._check_room(1)
        made = button(text, data, url=url, **fields)
        if self._open and len(self._rows[-1]) < self.width:
            self._rows[-1].append(made)
        else:
            self._rows.append([made])
            self._open = True

        self._count += 1
        return self

    def row(self, *buttons: InlineKeyboardButton) -> Self:
        if not 1 <= len(buttons) <= MAX_IN_ROW:
            raise KeyboardError(
                f"в ряду от 1 до {MAX_IN_ROW} кнопок, получено {len(buttons)}"
            )

        self._check_room(len(buttons))
        self._rows.append(list(buttons))
        self._open = False
        self._count += len(buttons)
        return self

    def markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[list(row) for row in self._rows])
