# selfrotgram

Асинхронная библиотека для Telegram Bot API на `aiohttp` и `pydantic`. Типы, методы и
фильтры генерируются из спецификации Bot API (10.3), поэтому в хендлерах не нужны ни
`assert x is not None`, ни `cast`: фильтр гарантирует поля, а тип это отражает.

Ставится как `selfrotgram`, импортируется как `selfrot`. Нужен Python 3.11+.

## Установка

Прямой ссылкой на репозиторий, как любая git-зависимость. В `pyproject.toml` проекта:

```toml
[project]
dependencies = [
    "selfrotgram @ git+https://github.com/SelfTopic/selfrotgram.git",
]
```

Дальше `poetry lock` и `poetry install`: Poetry запишет в `poetry.lock` конкретный коммит
(`resolved_reference`). Обновить до свежего коммита: `poetry update selfrotgram`.
Закрепить версию: `...selfrotgram.git@v0.1.0` (тег, ветка или коммит).
Без Poetry: `pip install "selfrotgram @ git+https://github.com/SelfTopic/selfrotgram.git"`.

Зависимости (`aiohttp>=3.12`, `pydantic>=2.11`, `typing_extensions>=4.14`) совместимы с
`aiogram 3.x`, поэтому обе библиотеки могут жить в одном окружении во время переезда.

## Минимальный бот

```python
import os

from selfrot import BaseContext, BaseDispatcher, Bot, MessageHandler
from selfrot.filter import Command
from selfrot.types import TextMessage


class Start(MessageHandler[BaseContext[TextMessage]]):
    query = Command("start")          # фильтр гарантирует, что text есть

    async def handle(self) -> None:
        await self.ctx.message.answer(f"Привет! Ты написал: {self.ctx.message.text}")


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Start,)


if __name__ == "__main__":
    Dispatcher(token=os.environ["BOT_TOKEN"]).start_polling()
```

Токен передаётся диспетчеру (`Dispatcher(token=...)`, откуда угодно: переменная окружения,
`pydantic-settings`). Без него читается `bot_token` из `bot_cfg.cfg` в текущей папке.
Настройки бота (`defaults`, `proxy`, таймауты) — в подклассе `Bot`, его указывают в `bot = MyBot`.

## Модульный проект

Роутеры собираются в дерево, хендлеры лежат в своих модулях, сервисы приложения
живут в своём `Context`:

```
myapp/
  __main__.py        # Dispatcher(...).start_polling() или start_webhook(...)
  context.py         # class AppContext(BaseContext[TEvent]): свои сервисы
  routers/
    profile.py       # class ProfileRouter(BaseRouter[AppContext]): handlers = (...)
    admin.py
```

```python
class Root(BaseDispatcher[AppContext]):
    bot = MyBot
    context = AppContext
    routers = (ProfileRouter, AdminRouter)       # или auto_connect = (".routers.profile",)
    middlewares = (LoggingMiddleware,)
```

## Что внутри

- **Фильтры:** `Text*`, `Command`, `CallbackData*`, `CallbackPayload` (типизированные
  данные кнопок), `Has*` (по одному на каждое поле), `MemberJoined`/`MemberLeft`,
  `FromUser`, комбинаторы `&`, `|`, `~`.
- **Типы и методы:** все объекты и методы Bot API, методы на самих объектах
  (`message.answer()`, `callback.answer()`, `sent.edit_text()`), `Bot.defaults`.
- **Диспетчер:** long polling и вебхуки, параллельная обработка, `on_startup`/`on_shutdown`,
  `on_error`, мидлвари с `pre_handle`/`post_handle`, корректная остановка по SIGTERM.
- **Клавиатуры:** `InlineKeyboard`, `button()` с проверкой лимитов Telegram.
- **Диалоги (FSM):** `States`, `State(Model)` с типизированными данными, `ctx.fsm`,
  `InState`, `MemoryStorage(ttl=...)`.

Подробно про решения и причины: [DESIGN.md](DESIGN.md).

## Разработка

```bash
poetry install                              # библиотека и dev-зависимости (pytest)
poetry run pytest                           # ~200 тестов, около 15 секунд, без сети
python -m examples.echo_bot                 # живой запуск примера, см. examples/README.md

python scripts/generate_types.py            # перегенерировать типы и методы из scripts/spec
python scripts/generate_types.py --fetch    # скачать свежую спецификацию
```

Тесты не ходят в Telegram: `tests/conftest.py` поднимает на localhost фейковый сервер Bot API
(`telegram`), записывающий все вызовы, и сборщики апдейтов. Каждый пример из `examples/`
дополнительно собирается в диспетчер в `tests/test_examples.py`, чтобы не устаревать.
