import logging
import os
from enum import Enum

from selfrot import (
    BaseContext,
    BaseDispatcher,
    Bot,
    CallbackPayload,
    CommandArgs,
    InlineKeyboard,
    MessageHandler,
    Rest,
)
from selfrot.filter import Command, HasReplyUser
from selfrot.handlers import CallbackQueryHandler
from selfrot.types import DataCallbackQuery, TextMessage

# Несколько веток одной команды внутри одного хендлера: каждый метод украшен фильтром
# как декоратором вместо того, чтобы заводить под каждую ветку свой класс. Первый
# подошедший декоратор побеждает — то же правило, что у роутера для списка хендлеров,
# только на уровень глубже, внутри одного класса.


class FunCommandsEnum(str, Enum):
    choice = "выбери"
    who = "кто"


class FunArgs(CommandArgs):
    command: FunCommandsEnum
    rest: Rest = ""


cmd = Command("fun", FunArgs)


class Fun(MessageHandler[BaseContext[TextMessage]]):
    # Query класса остаётся None (его сюда просто нельзя написать — см. docs/decisions.md),
    # а handle() не переопределяется: библиотека сама найдёт подошедшую ветку.

    @cmd.where(command=FunCommandsEnum.choice) & HasReplyUser()
    async def choice_reply(self) -> None:
        # HasReplyUser() в декораторе это проверил при check(), но заголовок класса — один
        # TextMessage на все ветки, так что сам редактор не сузит типы именно этой ветки.
        offender = self.ctx.message.reply_to_message.user  # type: ignore[union-attr]
        await self.ctx.message.reply(f"Выбираю {offender.first_name}!")  # type: ignore[union-attr]

    @cmd.where(command=FunCommandsEnum.choice) & ~HasReplyUser()
    async def choice(self) -> None:
        await self.ctx.message.reply("Выбираю... случайного участника чата!")

    @cmd.where(command=FunCommandsEnum.who)
    async def who(self) -> None:
        await self.ctx.message.reply("Случайный участник: вот ты!")


# Тот же механизм работает для любого вида хендлера — не только для MessageHandler.


class QuizAnswer(CallbackPayload, prefix="quiz"):
    option: int


OPTIONS = ["Гуль", "Человек"]


class Quiz(MessageHandler[BaseContext[TextMessage]]):
    query = Command("quiz")

    async def handle(self) -> None:
        keyboard = InlineKeyboard(width=2)
        for index, option in enumerate(OPTIONS):
            keyboard.button(option, QuizAnswer(option=index))
        await self.ctx.message.reply("Кто такой Канеки?", reply_markup=keyboard.markup())


class QuizPressed(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    @QuizAnswer.filter(option=0)
    async def gul(self) -> None:
        await self.ctx.callback_query.answer(f"Ты выбрал: {OPTIONS[0]}")

    @QuizAnswer.filter(option=1)
    async def human(self) -> None:
        await self.ctx.callback_query.answer(f"Ты выбрал: {OPTIONS[1]}")


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Fun, Quiz, QuizPressed)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
