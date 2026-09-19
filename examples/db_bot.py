import logging
import os
from typing import Optional, cast

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from selfrot import BaseContext, BaseDispatcher, BaseMiddleware, Bot, MessageHandler
from selfrot.filter import BaseFilter
from selfrot.types import Message, Update


class GreetingFormatter:
    """
    Аналог DialogService — не хранит per-update состояния,
    поэтому живёт весь процесс, а не создаётся на каждый апдейт.
    """

    def format(self, count: int) -> str:
        return f"Сообщений от тебя: {count}"


_DEFAULT_FORMATTER = GreetingFormatter()  # заглушка на уровне класса —
# create_context() перезаписывает её ДО того, как контекст кому-то
# виден, окна "ещё не установлено" не существует, поэтому Optional
# тут не нужен вовсе.


class Base(DeclarativeBase):
    pass


class UserStat(Base):
    __tablename__ = "user_stats"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    messages_count: Mapped[int] = mapped_column(default=0)


engine = create_async_engine("sqlite+aiosqlite:///./examples_db_bot.sqlite3")
session_factory = async_sessionmaker(engine, expire_on_commit=False)


class DBContext(BaseContext):
    _db: Optional[AsyncSession] = None
    fmt: GreetingFormatter = _DEFAULT_FORMATTER

    @property
    def db(self) -> Optional[AsyncSession]:
        return self._db

    @db.setter
    def db(self, value: AsyncSession) -> None:
        self._db = value


class DBMessageContext(DBContext):
    """
    Сюда попадает хендлер, только если HasMessageAndDB.check() уже
    подтвердил: апдейт — это message, и DatabaseMiddleware уже открыла
    сессию. Внутри хендлера — ни одного cast()/if на эти два поля.
    """

    @property
    def message(self) -> Message:
        return cast(Message, super().message)

    @property
    def db(self) -> AsyncSession:
        return cast(AsyncSession, super().db)

    @db.setter
    def db(self, value: AsyncSession) -> None:
        self._db = value
        # (мёртвый код в реальном пути: narrow() — это cast(), реальный
        # объект остаётся DBContext, этот сеттер никогда не вызовется.
        # Нужен только чтобы mypy/pyright не ругались на read-only
        # override read-write property.)


class HasMessageAndDB(BaseFilter[DBMessageContext]):
    async def check(self, ctx: BaseContext) -> bool:
        return ctx.message is not None and cast(DBContext, ctx).db is not None


class DatabaseMiddleware(BaseMiddleware[DBContext]):
    async def pre_handle(self) -> bool:
        self.session = session_factory()
        self.ctx.db = self.session
        return True

    async def post_handle(self, exc: Optional[BaseException] = None) -> None:
        if exc is not None:
            await self.session.rollback()
        else:
            await self.session.commit()

        await self.session.close()


class StatsHandler(MessageHandler[DBMessageContext]):
    query = HasMessageAndDB()

    async def handle(self) -> None:
        # ctx.message: Message, ctx.db: AsyncSession — оба гарантированы
        # HasMessageAndDB.check() ещё до вызова handle(). Ни одного
        # cast()/if на эти два поля тут больше нет.
        user = self.ctx.message.user
        if not user:
            # это НЕ обход Optional — from_user реально отсутствует
            # у постов в каналах/анонимных админов, это бизнес-решение
            # "не считаем такие сообщения", а не заглушка типизации.
            return

        stat = await self.ctx.db.get(UserStat, user.id)
        if stat is None:
            stat = UserStat(user_id=user.id, messages_count=0)
            self.ctx.db.add(stat)

        stat.messages_count += 1
        await self.ctx.db.flush()

        await self.ctx.answer_message(self.ctx.fmt.format(stat.messages_count))


class Dispatcher(BaseDispatcher[DBContext]):
    bot = Bot
    context = DBContext
    handlers = (StatsHandler,)
    middlewares = (DatabaseMiddleware,)

    def __init__(self, token: str | None = None) -> None:
        super().__init__(token)
        self.fmt = GreetingFormatter()  # один раз на весь процесс — "Singleton"

    def create_context(self, update: Update) -> DBContext:
        ctx = self.context(update, self.api)
        ctx.fmt = self.fmt  # тот же объект для всех апдейтов подряд
        return ctx

    async def setup(self) -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    import asyncio

    dp = Dispatcher(token=os.environ.get("BOT_TOKEN"))
    asyncio.run(dp.setup())
    dp.start_polling()
