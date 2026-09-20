import logging
import os
from contextvars import ContextVar, Token

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from selfrot import (
    BaseContext,
    BaseDispatcher,
    BaseMiddleware,
    Bot,
    MessageHandler,
    TEvent,
)
from selfrot.filter import HasUser
from selfrot.types import UserMessage

# База данных: одна сессия на один апдейт. Открываем в мидлвари, кладём в ContextVar,
# а хендлер получает её через ctx.db. Нужны пакеты sqlalchemy и aiosqlite.


class Base(DeclarativeBase):
    pass


class UserStat(Base):
    __tablename__ = "user_stats"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    messages_count: Mapped[int] = mapped_column(default=0)


engine = create_async_engine("sqlite+aiosqlite:///./examples_db_bot.sqlite3")
session_factory = async_sessionmaker(engine, expire_on_commit=False)
session_context: ContextVar[AsyncSession] = ContextVar("session_context")


class AppContext(BaseContext[TEvent]):
    @property
    def db(self) -> AsyncSession:
        return (
            session_context.get()
        )  # работает внутри хендлера, после DatabaseMiddleware


class DatabaseMiddleware(BaseMiddleware[AppContext]):
    session: AsyncSession
    _token: Token[AsyncSession]

    async def pre_handle(self) -> bool:
        self.session = session_factory()
        self._token = session_context.set(self.session)
        return True  # именно True: любое другое значение библиотека считает запретом

    async def post_handle(self, exc: BaseException | None = None) -> None:
        try:
            if exc is None:
                await self.session.commit()
            else:
                await self.session.rollback()  # хендлер упал: изменения не сохраняем
        finally:
            session_context.reset(self._token)
            await self.session.close()


class Stats(MessageHandler[AppContext[UserMessage]]):
    query = HasUser()  # у сообщения гарантированно есть отправитель

    async def handle(self) -> None:
        user = self.ctx.message.user  # User, а не Optional[User]
        stat = await self.ctx.db.get(UserStat, user.id)
        if stat is None:
            stat = UserStat(user_id=user.id, messages_count=0)
            self.ctx.db.add(stat)

        stat.messages_count += 1
        await self.ctx.message.answer(f"Сообщений от тебя: {stat.messages_count}")


class Dispatcher(BaseDispatcher[AppContext]):
    bot = Bot
    context = AppContext
    handlers = (Stats,)
    middlewares = (DatabaseMiddleware,)

    async def on_startup(self) -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def on_shutdown(self) -> None:
        await engine.dispose()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
