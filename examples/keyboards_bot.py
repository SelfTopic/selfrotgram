import logging
import os
from typing import Literal

from selfrot import BaseContext, BaseDispatcher, Bot, CallbackPayload, InlineKeyboard
from selfrot.filter import Command
from selfrot.handlers import CallbackQueryHandler, MessageHandler
from selfrot.types import DataCallbackQuery, TextMessage

# Порт кнопок из chestor_bot: quiz (InlineKeyboardBuilder + adjust(2)) и дуэль
# ("duel:<id>:<action>:<expected_telegram_id>" с ручным parse_duel_callback_payload).

OPTIONS = ["Гуль", "Человек", "Голубь", "Инспектор"]


class QuizAnswer(CallbackPayload, prefix="quiz"):
    question_id: int
    option: int


class Duel(CallbackPayload, prefix="duel"):
    duel_id: int
    action: Literal["consent_initiator", "consent_target", "fora_serious"]
    expected_id: int  # кто имеет право нажать: в группе кнопки видят все


class Quiz(MessageHandler[BaseContext[TextMessage]]):
    query = Command("quiz")

    async def handle(self) -> None:
        keyboard = InlineKeyboard(width=2)  # как builder.adjust(2)
        for index, option in enumerate(OPTIONS):
            keyboard.button(option, QuizAnswer(question_id=1, option=index))

        await self.ctx.message.reply("Кто такой Канеки?", reply_markup=keyboard.markup())


class QuizPressed(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    answer = QuizAnswer.filter()  # любые данные этого класса
    query = answer

    async def handle(self) -> None:
        data = self.answer.parse(self.ctx)  # QuizAnswer: option уже int
        await self.ctx.callback_query.answer(f"Ты выбрал: {OPTIONS[data.option]}")


class Challenge(MessageHandler[BaseContext[TextMessage]]):
    query = Command("duel")

    async def handle(self) -> None:
        user = self.ctx.message.user
        if user is None:
            return

        keyboard = InlineKeyboard().button(
            "Принять вызов",
            Duel(duel_id=1, action="consent_target", expected_id=user.id),
        )
        await self.ctx.message.answer("Вызов брошен!", reply_markup=keyboard.markup())


class Consent(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    """Кнопку нажал тот, для кого она (expected_id совпал с нажавшим)."""

    duel = Duel.filter(action="consent_target").pressed_by("expected_id")
    query = duel

    async def handle(self) -> None:
        data = self.duel.parse(self.ctx)
        # Правит сообщение под кнопкой без проверки isinstance(message, Message).
        await self.ctx.edit_message_text(f"Дуэль {data.duel_id} принята")


class NotForYou(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    """Та же кнопка, но нажал кто-то другой: хендлер ниже по списку ловит остальных."""

    query = Duel.filter(action="consent_target")

    async def handle(self) -> None:
        await self.ctx.callback_query.answer("Эта кнопка не для тебя", show_alert=True)


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Quiz, QuizPressed, Challenge, Consent, NotForYou)  # порядок важен


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
