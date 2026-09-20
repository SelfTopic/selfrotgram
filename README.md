# selfrotgram

Асинхронная библиотека для Telegram Bot API на `aiohttp` и `pydantic`, где **типы говорят
правду**: если хендлер обещает, что у сообщения есть текст, то фильтр это проверил, а
`message.text` в редакторе это `str`, а не `str | None`. Без `assert`, без `cast`, без
скрытых аргументов.

> Статус: альфа. Работает на реальном боте, покрыта тестами (200+), но API ещё может
> меняться. Поддерживает Bot API 10.3. Нужен Python 3.11+.

```python
class Echo(MessageHandler[BaseContext[TextMessage]]):    # обещаю: у сообщения есть текст
    query = HasText()                                    # проверяю: текст есть

    async def handle(self) -> None:
        await self.ctx.message.answer(self.ctx.message.text)   # text: str, проверять нечего
```

Забыли `HasText()`? Библиотека скажет об этом при запуске, а не сломается у пользователя.

## Чем это отличается

- **Ничего неявного.** Всё, что нужно хендлеру, лежит в `self.ctx`. Нет аргументов, которые
  «волшебно» появляются по имени, нет прокси `F`. Откуда что взялось, видно в коде.
- **Фильтр гарантирует, тип обещает, библиотека сверяет** (при импорте, а не в проде).
- **Всё, что скучно, уже есть.** Типы (400), методы (185), фильтры на каждое поле,
  ярлыки `ctx.answer_photo(...)`, методы на объектах (`message.edit_text(...)`) генерируются
  из официальной спецификации Telegram. Вышла новая версия Bot API, значит перегенерировали.
- **Типизированные диалоги и кнопки:** данные шага FSM и `callback_data` это модели с
  типами, а не словари и склеенные строки.

Знаете aiogram? [Сравнение с ним](docs/from-aiogram.md) с парами «было / стало».

## Установка

Прямой ссылкой на репозиторий, как любая git-зависимость. В `pyproject.toml` проекта:

```toml
[project]
dependencies = [
    "selfrotgram @ git+https://github.com/SelfTopic/selfrotgram.git",
]
```

Дальше `poetry lock` и `poetry install`: Poetry запишет в `poetry.lock` конкретный коммит.
Обновить до свежего: `poetry update selfrotgram`. Закрепить версию:
`...selfrotgram.git@v0.1.0` (тег, ветка или коммит). Без Poetry:
`pip install "selfrotgram @ git+https://github.com/SelfTopic/selfrotgram.git"`.

Ставится как `selfrotgram`, импортируется как `selfrot`. Зависимости (`aiohttp>=3.12`,
`pydantic>=2.11`, `typing_extensions>=4.14`) совместимы с `aiogram 3.x`, поэтому обе
библиотеки могут жить в одном окружении во время переезда.

## Минимальный бот

```python
import os

from selfrot import BaseContext, BaseDispatcher, Bot, MessageHandler
from selfrot.filter import Command
from selfrot.types import TextMessage


class Start(MessageHandler[BaseContext[TextMessage]]):
    query = Command("start")

    async def handle(self) -> None:
        await self.ctx.message.answer(f"Привет! Ты написал: {self.ctx.message.text}")


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Start,)


if __name__ == "__main__":
    Dispatcher(token=os.environ["BOT_TOKEN"]).start_polling()
```

Токен передаётся диспетчеру откуда угодно: переменная окружения, `pydantic-settings`. Без
него читается `bot_token` из `bot_cfg.cfg` в текущей папке. Настройки бота (`defaults`,
`proxy`, таймауты) задаются в подклассе `Bot`.

## Документация

| Что | Где |
|---|---|
| Каждый пример по шагам, простыми словами | [docs/examples.md](docs/examples.md) |
| Как устроена библиотека | [docs/design.md](docs/design.md) |
| Отличия от aiogram и что там было / что здесь | [docs/from-aiogram.md](docs/from-aiogram.md) |
| Работающие примеры (запуск: `python -m examples.echo_bot`) | [examples/](examples) |
| Журнал решений (для любопытных) | [docs/decisions.md](docs/decisions.md) |

## Что умеет

- **Фильтры:** `Text*`, `Command`, `CallbackData*`, `CallbackPayload` (типизированные данные
  кнопок, `pressed_by`), `Has*` (по одному на каждое поле), `MemberJoined`/`MemberLeft`,
  `FromUser`, `InState`; комбинаторы `&`, `|`, `~`.
- **Диспетчер:** long polling и вебхуки, параллельная обработка апдейтов, `on_startup` и
  `on_shutdown`, `on_error` на хендлере и диспетчере, остановка по SIGTERM.
- **Роутеры и мидлвари:** дерево роутеров (`auto_connect`), мидлвари с `pre_handle` и
  `post_handle(exc)`.
- **Диалоги (FSM):** `States`, `State(Model)` с типизированными данными, `ctx.fsm`,
  `MemoryStorage(ttl=...)`.
- **Клавиатуры:** `InlineKeyboard` с проверкой лимитов Telegram.
- **Транспорт:** таймауты, повтор при 429, понятные ошибки сети, прокси, `Bot.defaults`.

## Чего пока нет

Локализации, сцен, готового хранилища FSM в Redis, скачивания файлов и загрузки файлов
внутри альбомов, сборщика reply-клавиатур. Подробнее и честно:
[docs/from-aiogram.md](docs/from-aiogram.md#чего-здесь-нет-а-в-aiogram-есть).

## Разработка

```bash
poetry install                              # библиотека и dev-зависимости (pytest)
poetry run pytest                           # 200+ тестов, около 15 секунд, без сети
python -m examples.echo_bot                 # живой запуск примера, см. examples/README.md

python scripts/generate_types.py            # перегенерировать типы и методы из scripts/spec
python scripts/generate_types.py --fetch    # скачать свежую спецификацию
```

Тесты не ходят в Telegram: `tests/conftest.py` поднимает на localhost фейковый сервер Bot API,
записывающий все вызовы. Каждый пример из `examples/` дополнительно собирается в диспетчер в
`tests/test_examples.py`, чтобы не устаревать.
