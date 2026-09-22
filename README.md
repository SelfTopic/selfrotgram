# selfrotgram

[![CI](https://github.com/SelfTopic/selfrotgram/actions/workflows/ci.yml/badge.svg)](https://github.com/SelfTopic/selfrotgram/actions/workflows/ci.yml)

Асинхронная библиотека для Telegram Bot API на `aiohttp` и `pydantic`, где **типы говорят
правду**: если хендлер обещает, что у сообщения есть текст, то фильтр это проверил, а
`message.text` в редакторе это `str`, а не `str | None`. Без `assert`, без `cast`, без
скрытых аргументов.

> Статус: альфа. Работает на реальном боте, покрыта тестами (200+), но API ещё может
> меняться. Поддерживает Bot API 10.3. Python 3.11, 3.12 и 3.13 (проверяется в CI).

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

Знаете aiogram? [Сравнение с ним](https://github.com/SelfTopic/selfrotgram/blob/main/docs/from-aiogram.md) с парами «было / стало».

## Установка

```bash
pip install selfrotgram
poetry add selfrotgram
```

Обновить: `pip install -U selfrotgram` или `poetry update selfrotgram`. Poetry запишет `^0.1.4`,
то есть `>=0.1.4,<0.2.0`: пока версия `0.x`, ломающие изменения увеличивают минор (см.
[CHANGELOG.md](https://github.com/SelfTopic/selfrotgram/blob/main/CHANGELOG.md)).

Свежий коммит, ещё не вышедший на PyPI, или закреплённый тег ставятся прямо из git:

```bash
pip install "selfrotgram @ git+https://github.com/SelfTopic/selfrotgram.git"
poetry add "git+https://github.com/SelfTopic/selfrotgram.git#v0.1.4"
```

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

## Заготовка проекта: `selfrot init`

Библиотека ставит команду `selfrot`. В существующем проекте (там уже стоит `selfrotgram`):

```bash
selfrot init                 # создаёт src/bot (или selfrot init app/bot, другой путь)
selfrot init --dry-run       # только показать, что будет создано
```

```
.env.example                 BOT_TOKEN=...
src/bot/
  __main__.py                диспетчер и запуск (on_startup, on_shutdown, логирование)
  bot.py                     AppBot: настройки бота (defaults, proxy, таймауты) в комментариях
  context.py                 AppContext: сюда добавляются ваши зависимости
  routers/__init__.py        RootRouter: сюда подключаются остальные роутеры
  routers/start.py           стартовый /start, чтобы бот сразу отвечал
  keyboards/  middlewares/  filters/     пустые места под ваш код
```

Новый роутер: `selfrot add router` создаёт его и подключает в `RootRouter`:

```bash
selfrot add router profile            # routers/profile.py с примером хендлера
selfrot add router profile --module   # папка routers/profile/ с пустым роутером в __init__.py,
                                      # готовым принимать хендлеры из соседних модулей
```

Что уже есть в проекте, показывает `selfrot tree`: роутеры с мидлварями, хендлеры с видом
апдейта, обещанным типом и фильтром (сверху вниз это порядок проверки):

```
$ selfrot tree
Dispatcher  (мидлвари: LoggingMiddleware)
└─ RootRouter
   ├─ StartRouter
   │  └─ Start     message: TextMessage            Command('start')
   └─ AdminRouter  (мидлвари: OnlyAdmins)
      ├─ BanUser   message: TextMessage            (FromUser(1, 2) & Command('ban', Ban))
      ├─ Anything  message                         без фильтра: ловит всё этого вида
      ├─ Never     message: TextMessage            HasText()  ! недостижим: выше Anything ...
      └─ Joined    chat_member: ChatMemberUpdated  MemberJoined()

Роутеров: 3 (без корня), хендлеров: 4. allowed_updates: chat_member, message
```

Хендлер без фильтра ловит всё своего вида, и следующие за ним того же вида команда помечает как
недостижимые. Флаги: `-v` (переопределённые методы и описания), `--ascii`, `--package`.

Перед запуском или в CI `selfrot check` находит то, что при запуске не видно: собирает **все**
ошибки описания и импорта разом (обычный запуск остановился бы на первой), а ещё хендлер или
роутер, который нигде не подключён, хендлеры-дубли и недостижимые. `--strict` считает
предупреждения ошибками (код выхода 1).

```
$ selfrot check
Проверка src/bot: модулей 10, роутеров 3, хендлеров 6.
ошибка: src.bot.filters.oops: ModuleNotFoundError: No module named 'nonexistent_thing'
ошибка: src.bot.routers.broken: DefinitionError: NoGuarantee: в заголовке обещан TextMessage, но query None не гарантирует поля: text
предупреждение: src.bot.routers.admin: BanAgain недостижим: выше Ban тот же фильтр Command('ban')
предупреждение: src.bot.routers.admin: хендлер Forgotten нигде не подключён: добавьте его в handlers роутера
предупреждение: src.bot.routers.admin: роутер LostRouter не подключён: добавьте его в routers родителя ...
Итог: 2 ошибки, 4 предупреждения.
```

Создаётся только то, что касается самой библиотеки. Сервисы, база данных и структура бизнес-логики
остаются вашим делом. Существующие файлы команда **никогда не перезаписывает**. Запуск:
`BOT_TOKEN=... python -m src.bot`.

## Документация

| Что | Где |
|---|---|
| Каждый пример по шагам, простыми словами | [docs/examples.md](https://github.com/SelfTopic/selfrotgram/blob/main/docs/examples.md) |
| Как устроена библиотека | [docs/design.md](https://github.com/SelfTopic/selfrotgram/blob/main/docs/design.md) |
| Отличия от aiogram и что там было / что здесь | [docs/from-aiogram.md](https://github.com/SelfTopic/selfrotgram/blob/main/docs/from-aiogram.md) |
| Работающие примеры (запуск: `python -m examples.echo_bot`) | [examples/](https://github.com/SelfTopic/selfrotgram/tree/main/examples) |
| История изменений и правила версий | [CHANGELOG.md](https://github.com/SelfTopic/selfrotgram/blob/main/CHANGELOG.md) |
| Как выпускать версии на PyPI | [docs/releasing.md](https://github.com/SelfTopic/selfrotgram/blob/main/docs/releasing.md) |
| Журнал решений (для любопытных) | [docs/decisions.md](https://github.com/SelfTopic/selfrotgram/blob/main/docs/decisions.md) |

## Что умеет

- **Фильтры:** `Text*`, `Command`, `CallbackData*`, `CallbackPayload` (типизированные данные
  кнопок, `pressed_by`), `Has*` (по одному на каждое поле), `MemberJoined`/`MemberLeft`,
  `FromUser`, `InState`; комбинаторы `&`, `|`, `~`.
- **Аргументы команд как данные:** `CommandArgs` (типы, `Literal`, необязательные, `Rest`) и
  `CommandArgsError` с готовой подсказкой.
- **Отложенные действия:** `self.defer(fn, delay=...)` и `after_handle()`: сделать позже, уже после
  закрытия хендлера, не занимая слот и сессию БД.
- **Диспетчер:** long polling и вебхуки, параллельная обработка апдейтов, `on_startup` и
  `on_shutdown`, `on_error` на хендлере и диспетчере, остановка по SIGTERM.
- **Роутеры и мидлвари:** дерево роутеров (`auto_connect`), мидлвари с `pre_handle` и
  `post_handle(exc)`.
- **Диалоги (FSM):** `States`, `State(Model)` с типизированными данными, `ctx.fsm`,
  `MemoryStorage(ttl=...)`.
- **Клавиатуры:** `InlineKeyboard` с проверкой лимитов Telegram.
- **Файлы:** `ctx.download(путь)` — файл текущего апдейта сам; `bot.download(file_id)` — байты
  по id, без апдейта.
- **Транспорт:** таймауты, повтор при 429, понятные ошибки сети, прокси, `Bot.defaults`.

## Чего пока нет

Локализации, сцен, готового хранилища FSM в Redis, загрузки файлов внутри альбомов, сборщика
reply-клавиатур. Подробнее и честно:
[docs/from-aiogram.md](https://github.com/SelfTopic/selfrotgram/blob/main/docs/from-aiogram.md#чего-здесь-нет-а-в-aiogram-есть).

## Разработка

```bash
poetry install                              # библиотека и dev-зависимости (pytest)
poetry run pytest                           # 200+ тестов, около 15 секунд, без сети
python -m examples.echo_bot                 # живой запуск примера, см. examples/README.md

python scripts/generate_types.py            # перегенерировать типы и методы из scripts/spec
python scripts/generate_types.py --fetch    # скачать свежую спецификацию
```

На каждый пуш и pull request GitHub Actions запускает тесты на Python 3.11–3.13, проверку
типов (`pyright`), актуальность сгенерированного кода и установку пакета с командой `selfrot`.

Тесты не ходят в Telegram: `tests/conftest.py` поднимает на localhost фейковый сервер Bot API,
записывающий все вызовы. Каждый пример из `examples/` дополнительно собирается в диспетчер в
`tests/test_examples.py`, чтобы не устаревать.

## Лицензия

[MIT](https://github.com/SelfTopic/selfrotgram/blob/main/LICENSE).
