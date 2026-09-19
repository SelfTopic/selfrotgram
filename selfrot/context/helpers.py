from typing import Any

from ..client import Bot
from ..exceptions import ContextError
from ..types import CallbackQuery, Chat, Message, ReplyParameters, Update, User
from .accessors import EventAccessors, TEvent


class ContextHelpers(EventAccessors[TEvent]):
    """
    Откуда контекст берёт чат, пользователя и сообщение текущего апдейта. На этом
    строятся сгенерированные ярлыки (context/methods.py): ctx.answer_message(...),
    ctx.reply_message(...), ctx.delete_message() и остальные.
    """

    update: Update
    bot: Bot

    def _source_message(self) -> Message | None:
        """Сообщение апдейта: само событие или сообщение под кнопкой callback."""
        event = self.event
        if isinstance(event, Message):
            return event
        if isinstance(event, CallbackQuery) and isinstance(event.message, Message):
            return event.message

        return None

    @property
    def chat(self) -> Chat | None:
        event = self.event
        chat = getattr(event, "chat", None)
        if (
            chat is None
            and isinstance(event, CallbackQuery)
            and event.message is not None
        ):
            chat = event.message.chat

        return chat

    @property
    def chat_id(self) -> int:
        chat = self.chat
        if chat is None:
            raise ContextError(f"В этом апдейте ({type(self.event).__name__}) нет чата")

        return chat.id

    @property
    def user(self) -> User | None:
        """Отправитель события (у Telegram `from`, у реакций и опросов `user`)."""
        return getattr(self.event, "user", None)

    @property
    def message_id(self) -> int | None:
        """Сообщение апдейта (для callback — сообщение под кнопкой)."""
        event = self.event
        if isinstance(event, Message):
            return event.message_id
        if isinstance(event, CallbackQuery) and event.message is not None:
            return event.message.message_id

        return None

    def _require_message_id(self) -> int:
        message_id = self.message_id
        if message_id is None:
            raise ContextError(
                f"В этом апдейте ({type(self.event).__name__}) нет сообщения: "
                "передайте message_id явно"
            )

        return message_id

    def _send_defaults(self) -> dict[str, Any]:
        """Для отправки: бизнес-соединение и тема форума, как у исходного сообщения."""
        message = self._source_message()
        if message is None:
            return {}

        defaults: dict[str, Any] = {}
        if message.business_connection_id is not None:
            defaults["business_connection_id"] = message.business_connection_id
        if message.is_topic_message and message.message_thread_id is not None:
            defaults["message_thread_id"] = message.message_thread_id

        return defaults

    def _or_default(self, name: str, value: Any) -> Any:
        return value if value is not None else self._send_defaults().get(name)

    def _reply_parameters(self) -> ReplyParameters | None:
        message_id = self.message_id
        if message_id is None:
            return None

        return ReplyParameters(message_id=message_id)

    def _message_target(
        self,
        chat_id: Any,
        message_id: int | None,
        inline_message_id: str | None,
    ) -> tuple[Any, int | None, str | None]:
        """Что править: заданное явно, иначе сообщение апдейта, иначе inline."""
        if inline_message_id is not None:
            return chat_id, message_id, inline_message_id

        if chat_id is not None or message_id is not None:
            # Заданы только message_id (типичный «поправить своё сообщение»): чат
            # берём из апдейта, иначе запрос уйдёт без chat_id.
            if chat_id is None and self.chat is not None:
                chat_id = self.chat.id

            return chat_id, message_id, None

        if self.chat is not None and self.message_id is not None:
            return self.chat.id, self.message_id, None

        inline_id = getattr(self.event, "inline_message_id", None)
        if inline_id is not None:
            return None, None, inline_id

        raise ContextError(
            f"В этом апдейте ({type(self.event).__name__}) нечего править: "
            "передайте chat_id и message_id (или inline_message_id)"
        )

    def _event_id(self, field: str) -> str:
        event = getattr(self.update, field)
        if event is None:
            raise ContextError(f"В этом апдейте нет {field}")

        return event.id
