# Журнал решений

> Это **рабочие заметки автора**, а не документация: что решали, почему, что проверяли и
> что ещё не сделано. Много деталей переноса `chestor_bot`. Чтобы разобраться, как
> пользоваться библиотекой, читайте [путеводитель по примерам](examples.md), [как она
> устроена](design.md) и [отличия от aiogram](from-aiogram.md).

Живой журнал: обновляется вместе с кодом, а не отдельно от него.

## Зачем

Своя асинхронная библиотека для Telegram Bot API. Не "ещё один клон
aiogram" — попытка взять то, что реально нравится, из двух разных
экосистем:

- **aiogram** (Python) — эталон по охвату Bot API и структуре
  (Router/Filter/Middleware/FSM), но неудобный DX в мелочах.
- **grammY** (TypeScript) — эталон по эргономике `Context`: один объект,
  который сам знает, как ответить на то, что в нём лежит
  (`ctx.reply()`, `ctx.answerCallbackQuery()`), без ручного протаскивания
  `chat_id`/`message_id` по коду.

Финальная цель-маяк (не обязательство по срокам): суметь перенести на
эту библиотеку `chestor_bot` (197 файлов, aiogram 3 + SQLAlchemy +
боевой движок) и не переписывать при этом бизнес-логику насильно под
чужие ограничения.

## Текущее состояние (аудит на 2026-09-18)

Что реально есть и работает — проверено живым запуском (`examples/echo_bot.py`,
эхо через реальный `@nu_nuxua_sebe_bot`):

| Модуль | Статус |
|---|---|
| `client/Bot` | `Bot(BotMethods)`: `call()` шлёт метод и разбирает результат в тип (`TypeAdapter`), ошибки Telegram — исключения (`selfrot.exceptions`), токен из конструктора или конфига, `load_me()` |
| `client/session` (`AsyncSession`) | Работает: POST/GET через `aiohttp`, но не переиспользует `ClientSession` между вызовами аккуратно (создаётся один раз и живёт, ок) |
| `methods` | Все 185 методов Bot API 10.3: классы (`methods/generated.py`, dataclass с аргументами, `__returning__`) и методы `Bot` (`client/methods.py`, `bot.send_message(...)`). Сгенерированы |
| `types` | Все 400 типов Bot API 10.3 сгенерированы (`generated.py`) + 117 суженных `<Поле>Message` (`narrowed.py`), подключены через `selfrot.types`. Рукописных типов больше нет, кроме `HandlerType` |
| `dispatcher/BaseDispatcher` | Работает end-to-end (поллинг → middleware → handler → reply), но с багами (ниже) |
| `middleware` | Луковичная модель есть, реализован только `LoggingMiddleware` |
| `handlers` | `BaseHandler` + 26 видов по полям `Update` (`MessageHandler`, `EditedMessageHandler`, `CallbackQueryHandler`, `MyChatMemberHandler`, ...), сгенерированы (`handlers/kinds.py`) |
| `filter/base.py` | **Пустой файл**. Фильтров нет вообще |
| `router/base.py` | `BaseRouter`: handlers, middlewares и вложенные routers, поиск хендлера по дереву (см. «Router» ниже). `Dispatcher` — корневой роутер |
| `context/BaseContext` | `BaseContext[TEvent]`: `ctx.<поле Update>` (генерируется), `ctx.event`, помощники `ctx.chat`/`chat_id`/`user`/`message_id` и 123 ярлыка методов Bot (`ctx.answer_message`, `ctx.reply_message`, `ctx.answer_callback_query`, `ctx.delete_message`, ...) |
| `config/ConfigAPI` | Работает, читает/создаёт `.cfg` через `configparser` |

### Известные баги (не архитектура, а именно баги в текущем коде)

Пп. 1-3 и 5 (диспетчер) исправлены 2026-09-18, см. `dispatcher/dispatcher.py`.
Пп. 4, 6, 7 — ещё не тронуты, не входят в диспетчер.

1. ~~**`dispatcher.call_handler`** — если `handler.filter()` вернул `False`,
   метод делает `return None`, а не `continue`.~~ **Исправлено** — теперь
   `continue` (просто нет early return), непройденный фильтр не обрывает
   обработку остальных хендлеров.
2. ~~**`dispatcher.call_middleware`** — при провале `pre_handle()`
   обработка прерывалась без отката уже отработавших middleware.~~
   **Исправлено** — `post_handle()` теперь вызывается для всех
   middleware, чей `pre_handle()` успел пройти, независимо от того, был
   ли прерван весь цикл; `call_handler()` вызывается, только если все
   `pre_handle()` прошли.
3. ~~**`BaseDispatcher.handlers` / `.middlewares`** — мутируемые списки
   на уровне базового класса, расшариваются между инстансами.~~
   **Исправлено** — в `__init__` инстанс получает собственную копию
   (`self.handlers = list(self.handlers)`), не мутирует класс-атрибут.
4. ~~**`ConfigAPI.get_token`** — делает `print(token)`. Токен целиком
   печатается в консоль при каждом старте бота.~~ **Исправлено** — `print`
   удалён.
5. ~~**Поллинг без паузы и без long-polling `timeout`**~~ **Исправлено** —
   long polling (`polling_timeout = 30`), см. «Сеть».
6. ~~**`Message`/`CallbackQuery` pydantic-модели** — поля без `= None`
   делали ключ обязательным~~ **Исправлено** — типы сгенерированы, optional
   поля `Optional[...] = None`. Проверено: фото/стикер без текста, чат без
   `first_name`, пост канала без `from`, `callback_query`, `my_chat_member`
   разбираются через `Update(**u)` (путь `Bot.get_updates`).
7. ~~**`User.full_name`**~~ **Снято** — рукописный `User` удалён (нигде не
   использовался, как и `ChatType`, `Update.callback`, `Message.reply_message`
   с неверными именами полей).

## Целевая архитектура

Черновик, не финал — секции ниже стоит проходить по одной и фиксировать
решение перед реализацией.

### 1. Router + Filters (первый приоритет)

- `Router` — композируемый (`dp.include_router(sub_router)`), как в
  aiogram 3, а не плоский список хендлеров в диспетчере.
- Каждый хендлер регистрируется на роутере через декоратор:
  `@router.message(F.text == "/start")`.
- Filters — объекты с `__call__`/`check(ctx) -> bool`, комбинируемые
  через `&`, `|`, `~` (как aiogram `Filter`, а не строковые условия).
  Базовый набор: `Command`, `Text`, `StateFilter` (после FSM).

**Принято (реализовано, `selfrot/router/base.py`).** `Dispatcher` — корневой
`BaseRouter` (как в aiogram). Роутер — класс с атрибутами `handlers`,
`middlewares`, `routers` (классы, вложенные роутеры создаются родителем).

- Поиск хендлера: сначала собственные `handlers` роутера по порядку, потом
  вложенные `routers` по порядку, вглубь. Апдейт забирает первый подошедший.
- Мидлвари корня (Dispatcher) — **внешние**: на каждый апдейт, даже если
  хендлер не нашёлся. Мидлвари вложенного роутера — **внутренние**: только
  вокруг хендлера, найденного в его поддереве, от внешнего роутера к
  внутреннему. Иначе `GhoulMiddleware`/`ModeratorMiddleware` из `chestor_bot`
  (отвечают пользователю, ходят в БД и в Bot API) срабатывали бы на каждое
  сообщение, а не только на команды своей ветки. Как в aiogram.
- Блокировка (`pre_handle() -> False`) внутреннего мидлваря поглощает апдейт:
  дальше по дереву он не идёт. `post_handle` получают только те, чей
  `pre_handle` прошёл, и всегда, даже если хендлер упал.
- Следствие внутренней семантики: фильтры хендлеров выполняются до внутренних
  мидлварей, то есть фильтр не может опираться на данные, которые кладёт
  мидлварь роутера (как в aiogram). Тело хендлера — может.
- Объявления `handlers`/`middlewares`/`routers`/`auto_connect` — кортежи
  (`Sequence`), не списки: неизменяемые, так что общие на класс безопасно, а
  линтер (Ruff RUF012) не заставляют настраивать. `register_*` пересобирают
  кортеж у экземпляра, класс и соседние экземпляры не затрагиваются.
- Регистрация роутеров (порядок подключения = порядок поиска): сначала
  `routers = (Класс, ...)`, затем `auto_connect = ("путь.к.модулю", ...)`,
  затем метод `register_routers()` с вызовами `self.register_router(...)`.
  `register_router` принимает класс (создаётся) или экземпляр.
- `auto_connect`: строка — модуль или пакет, в котором лежит ровно один объект
  с именем `router` (класс или экземпляр `BaseRouter`). Папки не сканируются
  (порядок файлов определял бы приоритет). Путь с точкой считается от пакета
  модуля, где объявлен `auto_connect`. Пакет собирает своих детей тем же
  механизмом (свой `router` с `auto_connect`). Ошибки — на старте: модуль не
  найден, нет `router`, `router` не роутер, цикл в дереве (с цепочкой).
- Проверено на реальном дереве: `examples/chestor_routers` — 47 роутеров
  `chestor_bot` без хендлеров (42 листовых файла и 5 групп creator/ghoul/duel/
  moderator/chat_member; 19 в корне), мидлвари-заглушки на тех же роутерах. Порядок и состав сверены
  регулярками с кодом `chestor_bot`. Три слоя (`__init__` пакета, реэкспорт в
  `routers/__init__.py`, `routes.py`) стали одним списком `auto_connect` на
  каждом уровне. `python -m examples.chestor_routers` печатает дерево.
- Не сделано: собственные контексты роутеров (решим по ходу).
- Порядок мидлварей как в aiogram: первый в списке — самый внешний
  (`[Logging, Database]` даёт `Logging.pre Database.pre handler Database.post
  Logging.post`). Так же между роутерами: мидлвари родителя снаружи, вложенного
  внутри.
- Фильтры асинхронные (`async def check`): им нужно ходить в кеш и БД
  (как `RpCommandFilter` в `chestor_bot`). Данные во вложенный хендлер фильтр
  не передаёт — это делает `pre_handle` хендлера.

### 2. FSM

- Нужен для многошаговых сценариев (бои, прокачка в `chestor_bot`).
- Хранилище через интерфейс (`StorageBase`), реализация по умолчанию —
  in-memory, остальное (Redis и т.п.) — опционально, не обязаловка для
  ядра.
- `ctx.state.set(...)`/`ctx.state.get()` в духе grammY session-плагина,
  а не отдельный объект, который нужно доставать руками из DI.

### 3. Context — типизация по типу апдейта

- Один `BaseContext` — база, но для конкретных хендлеров (`MessageHandler`,
  `CallbackHandler`) контекст должен typing-гарантированно давать нужные
  поля (`ctx.message` не `Optional`, а обязательный, внутри
  `MessageHandler`).
- Методы-ответы по контексту: `answer_message`, `reply_message`,
  `answer_callback_query` и остальные ярлыки (см. «Ярлыки на контексте»).

**Принято (реализовано, `examples/bot_command`).** Цель — писать хендлер
без проверок и без своих фильтров:

```python
class BotHandler(MessageHandler[AppContext[TextMessage]]):
    query = Text("бот", ignore_case=True)
    # self.ctx.message.text здесь — str
```

- `BaseContext` обобщён по типу сообщения (`BaseContext[TMsg]`, `TMsg`
  ковариантный, по умолчанию `Optional[Message]`). Пользовательский
  контекст наследует `BaseContext[TMsg]` и остаётся с сервисами.
- Суженные типы сообщений (`TextMessage`, ...) поставляет библиотека:
  frozen-подкласс `Message`, где поле объявлено без `Optional`
  (`text: str = Field()`). Пользователь их не пишет.
- Фильтры поставляет библиотека (`Command`, `Text`, `CallbackData`, ...). Фильтр
  объявляет `guarantees` — тип сообщения, чьи поля `check()` уже проверил.
- Pyright не умеет выводить тип `self.ctx` из значения `query`, `.pyi` рядом
  с исходником при проверке самого исходника не используется (проверено),
  плагинов у Pylance нет. Поэтому узкий тип указывается в заголовке
  (`AppContext[TextMessage]`), а согласованность с `query` проверяется при
  создании класса (`BaseHandler.__init_subclass__`): заявлено больше, чем
  гарантирует фильтр, — `TypeError` на старте, а не `AttributeError` в
  проде.
- Какие поля тип обещает, считается по `get_type_hints` (`utils/narrowing.py`),
  а не по `model_fields`: pydantic теряет сужение от второй базы при
  множественном наследовании.
- Пока не решено: сужение того, что кладут мидлвари (`ctx.db`), идёт по
  старому пути (`BaseFilter.narrow` + подкласс контекста); комбинации
  «фото с подписью» и число видов сообщений в библиотеке. `/cmd@bot` в
  `Command` работает: диспетчер при старте зовёт `getMe` (`Bot.load_me`),
  `Bot.username` сверяется без учёта регистра. Комбинации фильтров решены,
  см. «Комбинаторы фильтров».

### Типы Bot API: генерация (`scripts/generate_types.py`)

Типы Bot API не пишутся руками, а генерируются из спецификации. Реализовано и
подключено: `selfrot.types` отдаёт сгенерированные типы (`from .generated import *`,
`from .narrowed import *`).

- Источник: `PaulSonOfLars/telegram-bot-api-spec` (`api.json`), закреплён в
  `scripts/spec/telegram-bot-api.json` (Bot API 10.3, 24.08.2026: 400 типов,
  185 методов). Обновить: `python scripts/generate_types.py --fetch`.
  Прежний кандидат (`ark0f/tg-bot-api`) отстал: версия 8.3 от февраля 2025, у
  `User` нет 5 полей, которые реально отдаёт `getMe`. Проверять версию, а не
  только что файл открывается.
- Результат: `selfrot/types/generated.py` (все типы, один модуль: нет
  циклических импортов) и `selfrot/types/narrowed.py` (по одному
  `<Поле>Message` на каждое optional-поле `Message`, 117 штук; для сужения
  через cast, в рантайме не создаются, сборка отложена).
- Модели frozen, лишние поля игнорируются (Telegram растёт), обязательные поля
  без `= None`, optional — `Optional[...] = None`. Поле `from` → `user` (alias
  `from`, как в `selfrot`; конфликтов с настоящим полем `user` в спеке нет).
  Описания полей — attribute docstring (видны при наведении в IDE).
- Объединения: если у всех подтипов есть поле с `always “x”` (`type`/`status`/
  `source`), это дискриминированный `Union` (`ChatMember`, `MessageOrigin`,
  `ReactionType`, ...), иначе обычный (`MaybeInaccessibleMessage`). `RichText`
  рекурсивный: `TypeAliasType`, объявлен до классов (иначе pyright
  отвергает ссылку на себя).
- Цена: импорт `generated`+`narrowed` ≈ 3 с (создание ~490 pydantic-классов,
  `defer_build` помогает только суженным: 2.8 → 0.6 с). Первая валидация
  `Update` ещё 0.2 с.
- Сгенерированные файлы помечены `# ruff: noqa` (иначе ~1100 замечаний при
  включённых UP-правилах); pyright по ним чист.
- Импорт `selfrot` теперь ≈ 2–5 с (обычный, без ленивой загрузки `narrowed`:
  решили пока не усложнять; вариант на потом — PEP 562 `__getattr__`).
- Суженные типы генерируются для `Message` (117) и для каждого объекта, который
  Bot API кладёт в `Update` (ещё 33: `DataCallbackQuery`, `MessageCallbackQuery`,
  `InviteLinkChatMemberUpdated`, `ExplanationPoll`, ...). Имя: `<Поле><Тип>`.
  `required_fields` определяет корень по MRO (ближайший класс из `generated`),
  поэтому работает для любого из них. Комбинации — наследованием в пределах
  одного корня.

### Комбинаторы фильтров (`selfrot/filter/base.py`)

`&`, `|`, `~` строят фильтр из фильтров; у хендлера по-прежнему один `query`.

```python
class Captioned(MessageHandler[AppContext[PhotoCaption]]):
    query = HasPhoto() & HasCaption()          # PhotoCaption = PhotoMessage + CaptionMessage
```

- Каждый фильтр отдаёт `guarantee()`: корневой тип Bot API и множество полей,
  которые `check()` уже проверил. Комбинатор считает итог сам:
  `a & b` — объединение полей, `a | b` — пересечение (обещают обе ветки),
  `~a` — ничего (только корень). Заголовок хендлера сверяется с итогом при
  создании класса: `HasPhoto() | HasCaption()` в заголовке `PhotoCaption` —
  `TypeError: ... не гарантирует поля: caption, photo`.
- Корни должны совпадать (`HasText & HasDataCallbackQuery` — `TypeError` при
  создании фильтра). Исключение — фильтр без `guarantees` (корень `None`):
  такой подходит любому виду обработчика и ничего не обещает.
- Свой фильтр — только `check()`, объявлять ничего не нужно. `HasText() &
  OnlyPrivate()` даёт `text`; `OnlyPrivate() | HasText()` — ничего (проверено).
- Вычисление ленивое, слева направо: правая часть `&` не зовётся после `False`,
  правая часть `|` — после `True`. Дорогой фильтр (БД, кеш) ставим справа.
- Аннотация `guarantees: type[...]` в подклассах убрана: перекрытие `ClassVar`
  ломало инвариантность в pyright, хватает присваивания `guarantees = TextMessage`.
- Pyright: `self.ctx.message.text` в `HasText() & Custom()` выводится как `str`;
  тип берётся из заголовка, комбинаторы на статику не влияют.

### Строковые фильтры и `Command` (`filter/strings.py`, `text.py`, `callback.py`, `command.py`)

Источник строки и способ сравнения собираются наследованием: `class Text(Equals,
TextSource)`. Семейства `Text*` (`message.text`, гарантирует `TextMessage`) и
`CallbackData*` (`callback_query.data`, гарантирует `DataCallbackQuery`) с
одинаковым набором: без суффикса (равно), `Startswith`, `Endswith`, `Contains`,
`Regexp`. Читают `ctx.event`, поэтому работают в любом виде обработчика.

```python
class Mut(MessageHandler[AppContext[TextMessage]]):
    pattern = TextRegexp(r"(\w+) мут (\d+)")
    query = pattern

    async def pre_handle(self):
        self.who, self.minutes = self.pattern.match(self.ctx).groups()

class Say(MessageHandler[AppContext[TextMessage]]):
    cmd = Command("бот скажи", prefixes="", ignore_case=True)   # или prefixes="/!"
    query = cmd
    async def handle(self): text = self.cmd.parse(self.ctx).rest
```

- Регистр: `ignore_case=False` по умолчанию, включается явно (`casefold`). Раньше
  `TextEquals` молча сравнивал без регистра — убран вместе с именем.
- **Результат разбора в фильтре не хранится**: `query` один на класс, а апдейты
  идут параллельно. Хендлер берёт его явно: `TextRegexp.match(ctx)` даёт
  `re.Match[str]`, `Command.parse(ctx)` — `CommandCall(prefix, args, rest)`.
  Возврат не Optional (никаких `assert` в хендлере); если вызвать без успешного
  `check()`, будет `LookupError`. Фильтр держим в атрибуте (`pattern`, `cmd`),
  а `query = pattern` — потому что pyright видит `self.query` как базовый
  `BaseFilter`, и методов подкласса на нём нет.
- `Regexp`: `re.match` (с начала строки), `full=True` — `re.fullmatch`.
- `Command`: имя из нескольких слов (`"бот скажи"`), `prefixes` — строка
  односимвольных префиксов (`"/!"`, `""` — без префикса), `args_count` точно.
  `@username` разбирается только с префиксом `/`. Имя с префиксом внутри —
  `ValueError` при создании.
- Ещё нет: те же семейства для `caption`, `inline_query.query`.

### Виды обработчиков и `ctx.<поле>` (сгенерировано)

Каждое поле `Update` — это отдельный вид обработчика, и разработчик выбирает его
явно (как `router.message` / `router.edited_message` в aiogram). Общего
«один message на все виды» нет.

```python
class Duel(CallbackQueryHandler[AppContext[DataCallbackQuery]]):
    query = DataStartsWith("duel:")

    async def handle(self):
        self.ctx.callback_query.data      # str
```

- Вид задаёт `update_field` и `payload_type` (`handlers/kinds.py`). Хендлер
  вызывается только когда заполнено именно это поле.
- Обработчик получает объект через `ctx.<имя поля>` (`ctx.message`,
  `ctx.edited_message`, `ctx.callback_query`, `ctx.my_chat_member`, ...).
  Тип берётся из заголовка: `AppContext[TextMessage]` даёт `ctx.message:
  TextMessage`, а `ctx.callback_query` в нём — ошибка типов (self-типизированные
  property). Без параметра `ctx.message` остаётся `Optional[Message]`.
  Параметр контекста переименован `TMsg` → `TEvent`.
- Фильтры не привязаны к полю: читают `ctx.event` (объект того поля, которое
  заполнено). Один `Command` работает и в `MessageHandler`, и в
  `EditedMessageHandler`. `guarantees` фильтра может быть любым типом Bot API.
- Проверка заголовка при старте: корневой тип заголовка совпадает с типом,
  который получает вид обработчика, и с типом `guarantees` фильтра, и фильтр
  гарантирует обещанные поля. Иначе `TypeError`.
- `allowed_updates` собирается из дерева (`used_update_types`) и уходит в
  `getUpdates`. Без него Telegram не присылает `chat_member`,
  `message_reaction`, `message_reaction_count` (проверено по докам). Тело GET
  Telegram читает так же, как query (проверено по `timeout`). Значение
  «липкое» на стороне Telegram: сброс — пустой список.
- Фильтры `Has*` (`selfrot/filter/has.py`, генерируются): по одному на каждый
  суженный тип, «у объекта вида заполнено поле». Имя: для `Message` короткое
  (`HasText`, `HasPhoto`, `HasCaption`, `HasUser`), для остальных с типом
  (`HasDataCallbackQuery`, `HasInviteLinkChatMemberUpdated`). Каждый
  гарантирует свой суженный тип, поэтому «ловить весь текст» — это
  `query = HasText()` в `MessageHandler[AppContext[TextMessage]]`. Приоритет —
  порядок в `handlers`: конкретные (`Command`) ставить выше `HasText`.
- Ограничения: `message`/`edited_message`/`channel_post`/... делят корневой тип
  `Message` (и `chat_member`/`my_chat_member` — `ChatMemberUpdated`), поэтому
  проверяющий типы не отличает `ctx.message` от `ctx.edited_message`: берите
  поле своего вида. `HandlerType`
  удалён (заменён видами).

### Методы Bot API (сгенерировано)

`bot.send_message(chat_id, text, *, reply_markup=..., ...)`: все 185 методов,
типизированные аргументы и результат.

- Аргументы: обязательные первыми (позиционные), необязательные после `*`
  (у 36 методов в спеке они перемешаны). Спека помечает необязательными и
  условно-обязательные (`editMessageText.text`: «если не задан
  `rich_message`»), поэтому у таких методов все аргументы именованные, а
  проверка остаётся на стороне Telegram.
- Результат разбирается в тип из спеки: `Message`, `List[Update]`,
  `Union[Message, bool]` (edit*: `Message` для чата, `True` для inline),
  дискриминированное `ChatMember`. Сообщение бота, отправленное через
  `answer_message`, теперь тоже `Message`, а не сырой dict.
- Передача: всегда POST. Без файлов — JSON (вложенные объекты без ручного
  `json.dumps`; модели сериализуются `by_alias`, `None` не отправляется, `False`
  и `0` отправляются). Есть `InputFile` (`types/input_file.py`) в аргументах —
  multipart (остальные аргументы рядом, объекты как JSON-строки). Строка
  (`file_id`/URL) в `InputFile | str` остаётся обычным JSON.
- Ошибки: `ok=false` → `TelegramBadRequest` (400), `TelegramUnauthorized`
  (401), `TelegramForbidden` (403), `TelegramNotFound` (404), `TelegramConflict`
  (409), `TelegramRetryAfter` (429, `.retry_after`), `TelegramServerError`
  (5xx), общий `TelegramAPIError`. Сетевые сбои — `TelegramNetworkError`, см.
  «Сеть». Диспетчер при старте (`getMe`) считает фатальными только 401/404.
- Проверено: локальный фейк-сервер (JSON, multipart, вложенные объекты,
  ошибки), живой Telegram (типизированные `get_*`, реальные ошибки), сквозной
  прогон `echo_bot` на реальных апдейтах.
- Ограничения: загрузка файлов только аргументом верхнего уровня
  (`send_photo(photo=InputFile(...))`); `attach://` для `send_media_group`
  и файлов внутри `InputMedia` не реализован (там пока только `file_id`/URL).

### Ярлыки на контексте (сгенерировано)

`ctx.answer_message("текст")`, `ctx.reply_message("текст")`,
`ctx.answer_callback_query(text="ок")`, `ctx.delete_message()`: те же методы, что
у `bot`, но чат, сообщение и id запроса берутся из текущего апдейта
(`context/methods.py`, 123 штуки). Старый `ctx.reply()` убран: он писал в чат
без цитаты, то есть был нынешним `answer_message`.

- `answer_<X>` для каждого `send<X>` с обязательным `chat_id` (24): пишет в чат
  апдейта. `reply_<X>` (21) то же, но с `reply_parameters` на сообщение
  апдейта; если сообщения нет (`my_chat_member`), цитаты просто нет.
- Как в aiogram, у отправки подставляются `business_connection_id` и
  `message_thread_id` (только для тем форума) сообщения апдейта; явный
  аргумент важнее.
- Ответы по id (`answer_callback_query`, `answer_inline_query`,
  `answer_shipping_query`, `answer_pre_checkout_query`): id берётся из
  апдейта, доступны по типам только в подходящем контексте
  (`AppContext[DataCallbackQuery]`), в контексте сообщений — ошибка типов.
- Правки (`edit_message_text`, `edit_message_caption`, ..., 17): цель — явные
  `chat_id`/`message_id`, иначе сообщение апдейта (для callback сообщение под
  кнопкой), иначе `inline_message_id`.
- Остальные методы с обязательным `chat_id` (`ban_chat_member`,
  `pin_chat_message`, `get_chat_member`, ...): `chat_id` из апдейта; если
  `message_id` обязателен, по умолчанию сообщение апдейта (`delete_message()`),
  но можно передать свой. Необязательный `message_id` не подменяется
  (`unpin_chat_message()` снимает последнее закреплённое, как в Bot API).
  `forward_message`/`copy_message`: `from_chat_id` и `message_id` из апдейта,
  `chat_id` (куда) явный. Для другого чата: `ctx.bot.<метод>(...)`.
- Если в апдейте нет нужного (у `InlineQuery`, `PollAnswer` нет чата; у
  `chat_member` нет сообщения), метод падает `RuntimeError` с понятным текстом,
  а не отправляет запрос в никуда.
- Проверено: фейк-сервер по видам апдейтов (сообщение, тема форума, business,
  callback с сообщением и inline, chat_member, inline_query), pyright
  (возвращаемые типы, отказ `answer_callback_query` в чужом контексте),
  живой Telegram (`echo_bot` на настоящем апдейте).

### Исключения (`selfrot/exceptions.py`)

Один модуль (как `aiogram/exceptions.py`); пакетом станет, когда разрастётся.
Все ошибки библиотеки наследуют `SelfrotError`, поэтому `except SelfrotError`
ловит любую. Пустые подклассы — намеренно: важен тип, а не тело.

| Класс | Когда | Совместим с |
|---|---|---|
| `TelegramAPIError` → `TelegramBadRequest`, `Unauthorized`, `Forbidden`, `NotFound`, `Conflict`, `ServerError`, `RetryAfter` | Bot API вернул `ok=false` (по HTTP-коду, поля `method`, `error_code`, `description`, `parameters`) | — |
| `TelegramNetworkError` → `TelegramTimeout` | не достучались до Telegram или не дождались ответа (обрыв, DNS, VPN); не имеет `error_code` | — |
| `ConfigError` | нет токена | — |
| `DefinitionError` | неверное описание при создании класса или фильтра: заголовок хендлера не совпал с `query`, фильтры разных типов в `&`/`\|`, `Command("")`, не роутер в `routers` | `TypeError` |
| `RouterError` | цикл в дереве, неверный путь `auto_connect` | `RuntimeError` |
| `ContextError` | ярлык не подходит апдейту: нет чата, сообщения, объекта | `RuntimeError` |
| `FilterMatchError` | `match(ctx)` / `parse(ctx)` вызван без успешного `check()` | `LookupError` |

Классы, которые раньше были встроенными исключениями, наследуют и их, чтобы
уже написанные `except TypeError`/`RuntimeError` не сломались. Голых
`raise Exception/RuntimeError/TypeError` в коде библиотеки не осталось
(`NotImplementedError` у абстрактных методов не считается).

### Сеть: таймауты, повторы, поллинг (`client/session.py`, `bot.py`, `dispatcher.py`)

Сделано под нестабильный канал (мобильный VPN). Проверено на локальном фейк-сервере:
429, 502 с HTML, медленный ответ, закрытый порт, сбой `getUpdates`, упавший хендлер.

- **Транспорт ничего не повторяет** и не пропускает чужие исключения наружу:
  `aiohttp.ClientError` → `TelegramNetworkError`, таймаут → `TelegramTimeout`,
  ответ не JSON (502 с HTML от прокси) → обычный `TelegramAPIError` по HTTP-коду
  (5xx → `TelegramServerError`). В тексте ошибки токена нет: aiohttp кладёт URL
  (`.../bot<TOKEN>/...`) в свои исключения, поэтому токен заменяется, а цепочка
  причин обрывается (`from None`).
- **Таймауты** задаются атрибутами класса `Bot` (диспетчер создаёт бота сам, так
  что настройка — подклассом: `class MyBot(Bot): request_timeout = 30`):
  `request_timeout = 60` на весь запрос, `connect_timeout = 10` на соединение
  (мёртвая сеть падает за 10 с, а не за 5 минут, как в умолчаниях aiohttp). Для
  `getUpdates` к таймауту добавляется его `timeout`, иначе каждый долгий пустой
  опрос считался бы обрывом.
- **Повтор — только там, где безопасно.** Обрыв соединения не повторяется: сообщение
  могло уйти, и повтор его продублирует. Повторяется только `429`: Telegram запрос
  не выполнил. `Bot.flood_retries = 3`, ждём `retry_after`, но не дольше
  `flood_max_wait = 30` с (иначе ошибка уходит в код). `flood_retries = 0` — выкл.
- **Long polling**: `BaseDispatcher.polling_timeout = 30` уходит в `getUpdates`;
  пауза 1 с осталась только для `polling_timeout = 0`.
- **Поллинг переживает сбои**: `SelfrotError` на `getUpdates` (сеть, 5xx, 409) —
  пауза 1, 2, 4 … 30 с (сброс после успеха), `TelegramUnauthorized` — остановка.
  Раньше цикл при ошибке крутился без паузы. Не-библиотечные ошибки (например,
  `ValidationError` от неразобранного апдейта) не глотаются: повтор не помог бы,
  апдейт остался бы тем же.
- **Ошибка в хендлере не роняет бота**: её ловит диспетчер, см. «Ошибки хендлеров».
  Раньше первый же `raise` в хендлере (в том числе сетевая ошибка при ответе)
  завершал `polling()`.
- **`Bot.close_session()`** вызывается в `finally` у `polling()` (без него
  «Unclosed client session»). Имя не `close`: это метод Bot API (`close`), он
  выводит бота с облачного сервера.
- Диагностика — через `logging` (`selfrot.*`, уровень WARNING), не `print`.

Ещё нет: повтор загрузки больших файлов.

### Ошибки хендлеров: `on_error` (`handlers/base.py`, `router/base.py`, `dispatcher.py`)

Исключения своих классов служат ответом пользователю. Сервис делает
`raise UserError("текст")`, а показывает его хендлер или диспетчер. Пример:
`examples/errors_bot.py`.

```python
class Rename(MessageHandler[...]):
    async def pre_handle(self): self.name = validate_name(...)   # raise UserError
    async def on_error(self, exc: Exception):
        if isinstance(exc, NotEnoughMoney): await self.ctx.reply_message(...); return
        raise exc                                                # не моё — выше

class Root(BaseDispatcher[...]):
    async def on_error(self, ctx, exc: Exception):
        if isinstance(exc, UserError): await ctx.reply_message(exc.message); return
        await super().on_error(ctx, exc)                         # лог
```

- **Цепочка из двух уровней:** `Handler.on_error(exc)` → `Dispatcher.on_error(ctx, exc)`.
  Контракт как у `except`: вернулся нормально — обработано; `raise exc` (так по
  умолчанию у хендлера) — идёт выше. У диспетчера по умолчанию лог. Роутерного
  уровня нет: это был бы роутер ошибок aiogram, для которого нет сценария;
  разная реакция выбирается `isinstance` внутри метода.
- **Порядок:** ошибка проходит сквозь мидлвари (`post_handle(exc)` откатывает
  сессию БД), и только потом вызывается `on_error`. Поэтому в нём недоступно
  `ctx.db`, а ответить пользователю (`ctx.reply_message`, вызов Bot API) можно.
  `Handler.on_error` вызывается, если хендлер уже найден (ошибка в его
  `pre_handle`/`handle` или в мидлвари вложенного роутера); иначе (упал фильтр
  или мидлварь диспетчера) ошибка идёт сразу в диспетчер.
- **Только `Exception`:** `CancelledError` и `KeyboardInterrupt` проходят насквозь,
  `on_error` для них не вызывается (остановка бота — не ошибка хендлера).
- **Свои ошибки отдельно от багов:** показывать пользователю `str(exc)` любого
  исключения нельзя (уйдёт «relation users does not exist»). Нужен маркерный
  класс (`UserError`) и `isinstance` на него. Библиотека такого класса не ставит:
  что считать «ошибкой для пользователя», решает приложение.
- **`pre_handle` — место для проверок:** упал → `handle` не вызывается, ошибка идёт
  в `on_error`.
- Если `on_error` (любого уровня) сам упал, диспетчер логирует это, бот живёт.
- **Найденный баг, исправлен:** цикл `pre_handle` мидлварей стоял вне `try`; если он
  падал у третьей мидлвари, у первых двух `post_handle` не вызывался (сессия БД не
  закрывалась). Теперь `post_handle` вызывается у всех, чей `pre_handle` прошёл;
  упавшая мидлварь в их число не входит. Известный остаток: если сам `post_handle`
  бросит исключение, `post_handle` внешних мидлварей не вызовутся.
- Проверено (`on_error` хендлера и диспетчера, `pre_handle` в хендлере, ошибка
  в мидлвари вложенного роутера, упавший фильтр, упавший `on_error`, отмена).

### Тесты и примеры (`tests/`, `examples/`)

Раньше проверки лежали во временных скриптах вне репозитория. Теперь это `pytest`
(`[tool.pytest.ini_options]`: `asyncio_mode = "auto"`, dev-группа в `pyproject.toml`).

- **Фейковый Telegram (`tests/conftest.py`).** Настоящий HTTP-сервер на localhost, в
  который на время теста подменяется адрес API. Записывает вызовы (`telegram.calls`,
  `.sent`, `.last()`), отвечает заготовками, ответ на метод задаётся через
  `telegram.on("метод", результат | функция | web.Response)`. Так проверяется весь
  путь: сериализация, транспорт, разбор ответа, а не подставные объекты. Сборщики
  апдейтов (`message_update`, `callback_update`) и `bind()` разбирают апдейт так же,
  как `Bot` и вебхук: объекты знают своего бота.
- **Что покрыто (204 теста, ~15 с):** фильтры и комбинаторы, проверка заголовка
  хендлера, `CallbackPayload`, клавиатуры и лимиты Telegram, статусы участников, FSM
  (включая TTL и диалог через диспетчер), маршрутизация, мидлвари (порядок, `ContextVar`,
  закрытие при падении `pre_handle`), `on_error`, `UpdateRunner`, порядок обновлений,
  жизненный цикл поллинга, транспорт (502, таймаут, обрыв, утечка токена и прокси, 429),
  `Bot.defaults`, вебхуки (секрет, дедупликация, 503, остановка), разбор типов, методы на
  объектах, ярлыки контекста, конструктор `Bot`. Проверены на Python 3.11.0 (версии
  прода) и 3.12.
- **Примеры** запускаются как `python -m examples.<имя>` с `BOT_TOKEN`, см.
  `examples/README.md`; `tests/test_examples.py` собирает каждый в диспетчер.
- **Не покрыто тестами:** реальный Telegram (нужен токен и публичный HTTPS для
  вебхуков), нагрузка, сгенерированные файлы целиком (проверяется выборочно: разбор
  типов и работа методов). Генератор не имеет своих тестов, и его результат в git
  проверяется только воспроизводимостью запуска.
- **CI (`.github/workflows/ci.yml`)**: на каждый пуш в `main` и на каждый pull request, четыре
  независимых задания (новый пуш в ту же ветку отменяет предыдущую проверку):
  1. **Тесты** на Python 3.11, 3.12, 3.13 (`pip install --group dev -e .`, `pytest`);
  2. **Типы:** `pyright selfrot examples scripts` (закреплена версия 1.1.414; ставится dev-группа,
     иначе примеры с `sqlalchemy` не разрешатся): «типы говорят правду» это главное
     обещание библиотеки, поэтому оно проверяется машиной;
  3. **Сгенерированный код совпадает с генератором:** `scripts/generate_types.py` и
     `git diff --exit-code`. Ловит забытую перегенерацию после правки генератора или
     спецификации;
  4. **Упаковка:** обычная (не editable) установка `pip install .` на Python 3.11 и в
     пустой папке `selfrot init`, `add router --module`, `check --strict`, `tree`: проверяет
     `poetry-core`, точку входа `selfrot` и то, что сгенерированный проект живой.
  Права `contents: read`, таймауты у каждого задания. `--group` требует pip 25.1+, поэтому
  pip обновляется первым шагом.
  **Проверено локально** каждым шагом в чистых окружениях (тесты на 3.11, 3.12 и 3.13: по 356
  прошли; pyright из PyPI с собственным node: 0 ошибок; перегенерация: без изменений; упаковка
  и CLI). Сам workflow на GitHub запустится только после пуша: до него поведение раннеров
  (версии действий, кэш) не проверено. Версии `actions/checkout@v4` и `setup-python@v5`
  указаны по памяти и могут потребовать обновления. Значок статуса добавлен в README.
  Python 3.13 добавлен в классификаторы после того, как весь набор тестов на нём прошёл.

### FSM: состояния диалогов (`selfrot/fsm/`, `filter/state.py`)

```python
class AgeStep(BaseModel): name: str
class ConfirmStep(AgeStep): age: int

class Register(States):
    name = State()                    # без данных
    age = State(AgeStep)              # состояние несёт тип своих данных
    confirm = State(ConfirmStep)

class GotAge(MessageHandler[AppContext[TextMessage]]):
    query = InState(Register.age) & HasText()
    async def handle(self):
        prev = await self.ctx.fsm.get(Register.age)                          # AgeStep
        await self.ctx.fsm.set(Register.confirm, ConfirmStep(name=prev.name, age=int(...)))
```

- **`ctx.fsm`** — небольшой объект `FSM`, который диспетчер прикрепляет к контексту
  апдейта. Сам ничего не хранит: собирается из хранилища диспетчера и ключа апдейта.
  Методы: `state()`, `set(state[, data])`, `get(state)`, `clear()`. Это не аргумент
  конструктора контекста (`init=False`), поэтому пользовательские контексты
  `self.context(update, api, сервисы...)` ничего не замечают. Контекст, созданный не
  диспетчером (тест), даёт `ContextError`.
- **Данные типизированы, а не `dict`.** `State(Model)` связывает состояние с моделью
  pydantic: `set(Register.age, AgeStep(...))` принимает только её, `get(Register.age)`
  возвращает `AgeStep`. Проверка типов ловит в редакторе неверную модель, `set` без
  данных для состояния с данными и `get` у состояния без данных. Убирает то, что у
  `chestor_bot` в `transfer_router`: `data.get("amount")` и `isinstance(amount, int)`
  с «сессия устарела». Накопление данных по шагам: модель следующего шага наследует
  предыдущую (`ConfirmStep(AgeStep)`), переход явный.
- **`fsm_key(ctx)`** — чей диалог: по умолчанию `"чат:пользователь"` (в группе у каждого
  свой сценарий, в личке чат совпадает с пользователем); переопределяется, как
  `ordering_key`. У апдейта без пользователя ключа нет: `state()` даёт `None`, а
  `set`/`get`/`clear` дают `FSMError`.
- **Хранилище:** интерфейс `Storage` (три метода `load`/`save`/`delete`, ключ строкой,
  значение `StoredState(name, data)` с JSON-словарём) и `MemoryStorage(ttl=...)` по
  умолчанию. `Dispatcher.fsm_storage = MemoryStorage(ttl=600)` задаёт своё; экземпляр
  у диспетчера свой (общий на класс делили бы все диспетчеры). Состояния пропадают при
  перезапуске, Redis и SQL — отдельными классами по тому же интерфейсу.
- **TTL — скользящее окно:** каждый `set` продлевает жизнь; брошенный диалог сам
  исчезает, и `InState` для него перестаёт совпадать (решает «сессия устарела»).
  Записи с истёкшим TTL вычищаются при записи, так что память не растёт.
- **Фильтры:** `InState(Register.age)`, `InState(Register)` (любой шаг группы), `NoState()`
  (нет диалога). Комбинируются: `Command("cancel") & ~NoState()`.
- **`InState` ничего не гарантирует про поля.** Шаг, читающий `ctx.message.text`,
  обязан писаться как `InState(...) & HasText()`, иначе заголовок с `TextMessage` не
  пройдёт проверку при импорте. Это то же правило «нет cast без гарантии», что и у
  остальных фильтров. Ответ на шаг ставят выше общих обработчиков текста: первый
  подошедший забирает апдейт.
- **Параллельность:** обработка апдейтов идёт параллельно, поэтому два быстрых
  сообщения одного пользователя в диалоге могут гоняться за состояние. Для FSM-ботов
  включают порядок (`ordering_key` → `order_by_user`), см. «Параллельная обработка».
- Проверено: 35 сценариев (состояния, TTL и его продление и чистка, ошибки, ключи по
  чату и пользователю, многошаговый диалог с отменой через диспетчер), под Python 3.11
  и 3.12. Состояний в общем хранилище с Redis/SQL пока нет.

### Пакет и установка (`pyproject.toml`)

Библиотека подключается **так же, как `ghoul-quiz-lib` в `chestor_bot`**: прямой ссылкой
`"selfrotgram @ git+https://github.com/SelfTopic/selfrotgram.git"` в
`[project].dependencies`; Poetry записывает коммит в `poetry.lock`
(`type = "git"`, `resolved_reference`).

- **Сборка как у их библиотеки:** `poetry-core>=2.0.0,<3.0.0`, метаданные PEP 621 в
  `[project]`, `[tool.poetry] packages = [{include = "selfrot"}]`. Дистрибутив
  `selfrotgram`, импорт `selfrot`. `py.typed` в пакете, поэтому Pylance у потребителя
  видит типы (фильтры сужают `self.ctx.message.text` до `str`).
- **Python 3.11+**, а не 3.12: боевой `Dockerfile` бота это `python:3.11-slim`, и
  `requires-python = ">=3.11,<3.15"` у самого бота. Первая версия `pyproject` требовала
  3.12 и не поставилась бы. Проверено на 3.11.0.
- **Зависимости:** `aiohttp>=3.12`, `pydantic>=2.11`, `typing_extensions>=4.14`. Границы
  выбраны по версиям из `poetry.lock` бота (aiohttp 3.12.15, pydantic 2.11.7,
  typing-extensions 4.14.1; у бота `aiohttp<3.13`, а `aiogram 3.31` требует
  `pydantic<2.14`), поэтому обе библиотеки живут в одном окружении. Только эти три:
  SQLAlchemy и остальное нужны примерам, а не библиотеке.
- **Побочные эффекты убраны:** `Bot("токен")` раньше при каждом создании писал
  `bot_cfg.cfg` в текущую папку потребителя. Теперь файл читается только при
  `Bot()` без токена. Токен проверяется по формату (`123456:ABC...`), заглушка
  `YOUR_BOT_TOKEN` из старого конфига даёт `ConfigError`, а не `ValueError` из `int()`.
- **Что проверено:** сборка из git-копии, `poetry lock` и `poetry install` в
  отдельном проекте (Python 3.11), импорт из установленного пакета, все проверки
  под Python 3.11.0 с зафиксированными у бота `pydantic 2.11.7`,
  `aiohttp 3.12.15`, `typing_extensions 4.14.1`.
- **Лицензия: MIT** (`LICENSE`, `Copyright (c) 2026 CheStor`, `license = {text = "MIT"}` и
  классификатор в `pyproject.toml`, как у `ghoul-quiz-lib`). Выбрана как самая привычная в
  Python-экосистеме (aiogram, pydantic; aiohttp под Apache-2.0, совместима) и совпадающая с
  лицензией `chestor_bot`; GPL/AGPL сузили бы круг пользователей библиотеки и заставили бы
  открывать боты на ней. Проверено: `LICENSE` попадает в колесо (`dist-info/licenses/`) и в
  sdist, метаданные `License: MIT` и `License-File: LICENSE`.
- **PyPI.** Мотив автора: `pip install selfrotgram` без `git` на
  машине. Публикация автоматическая, из `.github/workflows/publish.yml`, **без токена**
  (trusted publishing: PyPI доверяет паре репозиторий + файл + окружение); порядок и
  настройка: `docs/releasing.md`. Встроено: только с тега на настоящий PyPI, версия обязана
  совпасть с тегом, `id-token: write` только у заданий публикации, репетиция на TestPyPI
  ручным запуском, окружение `pypi` можно закрыть подтверждением. `twine check --strict`
  добавлен и в обычный CI. При подготовке нашлось: README с относительными ссылками
  (`docs/...`) на PyPI дал бы 404 (PyPI показывает README без репозитория), ссылки сделаны
  абсолютными; в метаданные добавлены `Documentation`, `Changelog`, `Issues`. Содержимое
  колеса проверено: только `selfrot/` (65 файлов), `py.typed`, `LICENSE`, точка входа, ни
  тестов, ни примеров. **Не проверено:** сам workflow на раннерах и приём пакета PyPI
  (нужны аккаунты и настройка издателя на стороне PyPI, это делает автор в браузере).
  Имя `selfrotgram` свободно на 2026-09-20; версию на PyPI перезаписать нельзя.
  **Версия первого выпуска: 0.1.1, а не 0.1.0** (выбор автора). Тег `v0.1.0` уже стоял на
  коммите без `publish.yml`, без ссылок проекта и с относительными ссылками в README; выпуск с
  него дал бы худшую страницу на PyPI, которую потом нельзя исправить. Перевешивать
  опубликованный тег (принудительный пуш) не стали: `0.1.0` остаётся только тегом в git.
  Окружение `pypi` на GitHub требует подтверждения автора и принимает только теги `v*`;
  `testpypi` открыто для ручной репетиции.
- **Файл `logging`:** случайный 12-МБ вывод ImageMagick (коммит `b403dbc`) удалён из текущего
  состояния (`6f2997d`). В истории он остаётся: в упакованном виде это около 1 МБ из всего
  `.git`, поэтому переписывать историю (принудительный пуш в публичный репозиторий) решили
  не делать.

### Мидлвари уровня апдейта (`dp.update.middleware` у `chestor_bot`)

В `__main__` прода четыре: `Logging` → `Database` → `SyncEntities` → `Ban` (первая
снаружи). Плюс по одной на роутер: `Ghoul`, `Creator`, `Moderator`, `RpCommands`.
Проверено прототипом на нашем API (фейковые сессии, реальный Bot API-сервер-заглушка):

| Что делает у прода | У нас |
|---|---|
| `dp.update.middleware` работает на каждый апдейт, даже без найденного хендлера | мидлвари диспетчера (внешние), проверено |
| обёртка `await handler(...)`, можно не вызвать (бан, `Ghoul`, `Creator`) | `pre_handle() -> bool`: `False` — хендлер не вызывается; ответить пользователю можно тут же (`ctx.answer_message`, `ctx.answer_callback_query(show_alert=True)`) |
| `DatabaseMiddleware`: `try: handler; commit; except: rollback; finally: reset` | `pre_handle` открывает, `post_handle(exc)` коммитит при `exc is None`, иначе откатывает |
| `Logging`: время вокруг всей цепочки | `pre_handle`/`post_handle` самой внешней мидлвари |
| `SyncEntities` в своей сессии с коммитом до хендлера | `pre_handle`, `post_handle` пустой |
| `Ban`: вытаскивает пользователя из `Update` цепочкой `isinstance` | `self.ctx.user` для любого вида апдейта |
| `router.message.middleware` + `router.callback_query.middleware` | одна мидлварь роутера на всё поддерево (любой вид), ограничение по виду — в самой мидлвари |

- **Найден и исправлен баг, ломавший прод-схему с `ContextVar`.** `pre_handle` и
  `post_handle` запускались через `asyncio.create_task`, то есть в дочерней задаче:
  значение `session_context.set(session)` не доходило до хендлера, а
  `session_context.reset(token)` падал (`token was created in a different Context`).
  На этом держится весь DI прода (`db_session = Factory(lambda: session_context.get())`).
  Теперь `pre_handle`, `handle` и `post_handle` идут в одной задаче; параллельные
  апдейты не путают значения (у каждой задачи свой контекст, проверено).
- **Исправлен `LoggingMiddleware`:** «мс» были секундами (`int(time.time() - start)`
  без `* 1000`), время считалось `time.time()` вместо `monotonic()`; добавлен
  пользователь.
- **Открыто: типизированные данные из мидлвари в хендлер.** У прода это один случай на
  весь бот (`data["rp_commands"]` в `RpCommandsMiddleware`). Пока для такого хватает
  `ContextVar` (как `session_context`); отдельный механизм «мидлварь гарантирует поля
  ctx» (по аналогии с `guarantees` у фильтров) не делаем, пока случаев мало.
- **Решено: порядок по чату против долгих хендлеров.** Docstring `SyncEntities` у
  прода описывает боль от долгих хендлеров (нарезка видео в `anime_router`, десятки
  секунд), а aiogram обрабатывает апдейты одного чата параллельно. Поэтому у нас
  порядка по умолчанию нет (`ordering_key` возвращает `None`), включается явно, см.
  «Параллельная обработка». Поведение порта совпадает с продом.

### Методы на объектах: `message.answer()`, `callback.answer()` (генерируются)

Решено: у `Message`, `CallbackQuery`, `InlineQuery`, `ShippingQuery`,
`PreCheckoutQuery`, `ChatMemberUpdated` есть методы, как у aiogram. Пример из порта:

```python
processing = await msg.reply("⏳ Начинаю нарезку")
await processing.edit_text("почти готово")
await processing.delete()
await ctx.callback_query.answer("готово", show_alert=True)
await ctx.chat_member.answer("Добро пожаловать!")
```

- **Как объект знает бота.** `Bot.call` и вебхук разбирают ответ с контекстом
  валидации `{"bot": bot}`; базовая модель `_Base.model_post_init` кладёт бота в
  приватный атрибут, включая вложенные (`reply_to_message`, `callback.message`).
  Объект, созданный вручную (`Update(...)` в тесте), к боту не привязан: метод даёт
  `BotNotBoundError` с пояснением. Приватный атрибут входит в `==`, поэтому
  привязанное и непривязанное сообщение с одинаковыми полями не равны.
- **Генерация из спеки** (`bound_methods` в генераторе, тот же принцип, что у
  ярлыков контекста): методы `send*` дают `answer`/`answer_photo` и
  `reply`/`reply_photo` на `Message` и `answer*` на `ChatMemberUpdated`; методы с
  `chat_id` + `message_id` — `edit_text`, `edit_caption`, `edit_media`,
  `edit_reply_markup`, `delete`, `pin`, `unpin`, `stop_poll`, `set_reaction`, ...;
  `forward(chat_id)` и `copy_to(chat_id)`; `answer*Query` — `answer` на
  `CallbackQuery`/`InlineQuery`/`ShippingQuery`/`PreCheckoutQuery`. Имя строится
  из имени метода без `_message`/`_chat_message` (`delete_message` → `delete`), а
  конфликты с полями и друг с другом генератор ловит на этапе генерации.
- `answer` берёт чат сообщения и переносит `business_connection_id` и тему форума,
  `reply` ещё и цитирует сообщение (как `ctx.answer_message`/`reply_message`).
  `edit_*`, `delete`, `pin` правят именно это сообщение; чужое — через `ctx` или бота.
- Всё идёт через `Bot.call`, поэтому `Bot.defaults` и повтор при 429 действуют.
- **Основное поле — позиционное**, хотя в спеке оно необязательное (текст или
  `rich_message`): `edit_text("...")`, `edit_caption("...")`, `callback.answer("...")`,
  так же у `ctx.edit_message_text` и `ctx.answer_callback_query`.
- Суженные типы (`TextMessage`) наследуют методы. Стоимость: `generated.py` вырос с
  6 тыс. до 10 тыс. строк, время импорта прежнее.

### CLI: `selfrot init` (`selfrot/cli/`)

Идея автора: генерировать «предпочитаемое дерево проекта». Граница проведена автором:
**только то, что касается самой библиотеки**. Структура service/repository это решение
бизнес-логики, а не библиотеки (для большинства ботов это перебор), и БД библиотека знать не
может. Поэтому в заготовке нет ни `services/`, ни `repositories/`, ни `database/`, ни `pyproject`.

- **`init`, а не `new`.** CLI входит в установленную библиотеку, значит проект и его
  `pyproject.toml` уже существуют, а `selfrotgram` уже стоит. Команда только добавляет файлы.
- **Дерево:** `.env.example` в текущей папке и `src/bot/` (`src/__init__.py`,
  `__init__.py`, `__main__.py`, `bot.py`, `context.py`, `routers/{__init__,start}.py`,
  пустые `keyboards/`, `middlewares/`, `filters/`). Путь пакета настраивается
  (`selfrot init app/bot`, `selfrot init mybot`); имена проверяются как идентификаторы Python.
- **Диспетчер живёт в `__main__.py`.** Он и есть точка входа, там же логика запуска
  (`on_startup`, `on_shutdown`); отдельного `dispatcher.py` нет.
- **Пять решений сверх списка автора**, чтобы сгенерированный бот не был сюрпризом:
  1. стартовый `routers/start.py` (`/start`), подключённый к `RootRouter`: без хендлеров бот
     молчал бы, а `allowed_updates` был бы пустым;
  2. `logging.basicConfig` и `LoggingMiddleware`: без них работающий бот выглядит зависшим;
  3. токен: если `BOT_TOKEN` не задан, остановка с понятным сообщением, а не молчаливое
     чтение `bot_cfg.cfg` (библиотека `.env` не читает и зависимость от `python-dotenv` не
     навязывает);
  4. пустые `__init__.py` в `src/` и `src/bot/`;
  5. `.gitignore` не правится, а команда напоминает добавить `.env`.
- **Роутеры подключаются явно:** `RootRouter.routers = (StartRouter,)` через обычный импорт
  (проверяется редактором); `auto_connect` оставлен в комментарии как вариант.
- **Безопасность:** существующие файлы не перезаписываются (пропускаются и перечисляются),
  есть `--dry-run`; недопустимый путь даёт ошибку без трейсбека, ничего не создав.
- **Реализация без зависимостей:** `argparse`, шаблоны строками в `cli/templates.py`
  (никаких файлов данных, которые могли бы потеряться при упаковке), запуск как
  `selfrot` (`[project.scripts]`) и `python -m selfrot`.
- **Проверено:** 24 теста (точное дерево и пустота пустых мест, `--dry-run`, повторный запуск
  не трогает правки, другие пути, ошибки путей, сгенерированный проект импортируется, строит
  диспетчер, отвечает на `/start` через фейковый Telegram, без токена останавливается и не
  создаёт `bot_cfg.cfg`; `python -m selfrot`), `pyright` чист на сгенерированном коде,
  установка на чистый Python 3.11 даёт работающую команду `selfrot`.
- **`selfrot add router <имя> [--module] [--package путь] [--dry-run]`.** Создаёт роутер и
  подключает его в `RootRouter`:
  - **файл** `routers/<имя>.py` с примером хендлера (`/<имя>`), либо с `--module` **папку**
    `routers/<имя>/__init__.py` с пустым роутером (`handlers = ()`), готовым принимать
    хендлеры из соседних модулей (идея автора). Внутри папки на уровень глубже, поэтому в
    её модулях `context` импортируется тремя точками (`from ...context import AppContext`);
    это сказано в комментарии шаблона и проверяется тестом (хендлер рядом с `__init__`);
  - **подключение по меткам** `# selfrot: imports` и `# selfrot: routers` в шаблоне
    `RootRouter`: импорт и элемент кортежа вставляются перед метками, поэтому порядок
    подключённых сохраняется (первый подошедший хендлер побеждает), а метки остаются для
    следующих вызовов. Если меток нет (файл переписан вручную), команда **ничего не
    правит** в чужом коде, создаёт сам роутер и печатает две строки для ручной вставки.
    Автоподхват без правок (обход папки) не делали: список роутеров и их порядок должны
    быть видны в коде;
  - импорт в `RootRouter` одинаков для файла и папки (`from .profile import ProfileRouter`),
    поэтому файл можно позже превратить в папку, не трогая корневой роутер;
  - имя: строчные латинские буквы, цифры и `_`, с буквы; `user_stats` даёт `UserStatsRouter`;
  - существующий роутер (файл или папка) это ошибка без изменений; без `selfrot init`
    ошибка с подсказкой; код выхода 1 и сообщение без трейсбека;
  - проверено: 34 теста, `pyright` чист на сгенерированном коде, добавленный роутер отвечает
    через фейковый Telegram.
- **`selfrot tree [модуль:класс] [--package путь] [-v] [--ascii]`** (идея автора: показывать не
  одно дерево роутеров, а роутеры, хендлеры и их фильтры). Строит диспетчер проекта и
  печатает:
  - роутеры с мидлварями (`мидлвари: A, B`), хендлеры с **видом апдейта и обещанным типом**
    (`message: TextMessage`, из заголовка) и **фильтром** (`repr` фильтра);
  - **порядок сверху вниз это порядок проверки** (свои хендлеры роутера, потом вложенные
    роутеры): побеждает первый подошедший;
  - **хендлер без фильтра** помечен «ловит всё этого вида», а все следующие за ним того же
    вида получают предупреждение «недостижим: выше X без фильтра» (обход дерева и есть порядок
    диспетчера, поэтому предупреждение точное; хендлеры других видов не затрагиваются).
    Более сложные случаи (фильтр-надмножество) не ищутся: ложные срабатывания хуже
    молчания;
  - итог: число роутеров и хендлеров, `allowed_updates`; `-v` добавляет переопределённые
    методы (`pre_handle`, `after_handle`, `on_error`) и первую строку docstring.
  - **Без сети и токена:** диспетчер создаётся с заглушкой токена, `getMe` не вызывается,
    файлы не пишутся. Цель по умолчанию `<пакет>.__main__:Dispatcher`, иначе `модуль:класс`.
    Ошибки импорта и создания показываются сообщением, а не трейсбеком.
  - **Для читаемости улучшены `repr` фильтров:** `Command('calc', CalcArgs, prefixes='/!',
    ignore_case=True, strict=True)`, `Text('бот', ignore_case=True)`, `TextRegexp('..',
    full=True)`. Рамки дерева заменяются обычными символами, если терминал (например,
    cp1251) не умеет их печатать.
  - проверено: 22 теста, включая порядок, недостижимые хендлеры, `-v`, `--ascii`, ошибки,
    `python -m selfrot tree`.
- **`selfrot check [модуль:класс] [--package путь] [--strict] [-v]`.** Что даёт сверх обычного
  запуска: импорт останавливается на первой ошибке, а `check` импортирует **каждый модуль
  пакета отдельно** и показывает все ошибки разом (синтаксис, отсутствующий модуль,
  `DefinitionError` заголовка хендлера, `SystemExit` в модуле), затем собирает диспетчер
  (его ошибка, например неверный `auto_connect`, тоже ошибка) и ищет то, что в рантайме не
  видно:
  - **забытые подключения:** хендлер, объявленный в проекте, но не стоящий ни в одном
    `handlers`, и роутер, не подключённый к родителю (самая частая ошибка: файл создан,
    строку в кортеж не добавили). Класс, от которого в проекте наследуют, не считается
    забытым (общий базовый хендлер);
  - **недостижимые хендлеры:** выше стоит хендлер того же вида без фильтра или **с тем же
    фильтром**. Одинаковыми считаются только фильтры, чей `repr` честно печатает все
    параметры (встроенные и комбинаторы из них, с проверкой одного и того же класса модели
    аргументов и payload); у пользовательских фильтров `repr` по умолчанию скрывает
    параметры (`IsUser(1)` и `IsUser(2)` оба печатаются как `IsUser()`), их не сравниваем,
    чтобы не было ложных срабатываний;
  - один и тот же хендлер подключён дважды; нет ни одного хендлера вообще.
  Ошибки дают код выхода 1; предупреждения только с `--strict` (для CI). Общий разбор порядка
  хендлеров (`cli/analysis.py`) используется и в `tree`, так что «недостижим» там теперь
  тоже показывает «тот же фильтр». Пустой роутер не предупреждение: только что созданный
  `add router --module` пуст намеренно, и в CI со `--strict` заготовка проходила бы.
  Проверено: 22 теста (все ошибки разом, `SystemExit`, ошибка диспетчера, забытые хендлеры и
  роутеры, базовый класс, дубли, ложные срабатывания пользовательских фильтров, `--strict`,
  `-v`, `python -m selfrot check`).
- **Не нужно:** `add` для мидлварей и фильтров (решение автора: они пишутся руками, ничего
  библиотечного в заготовке нет).

### Отложенные вызовы: `defer` и `after_handle` (`deferred.py`)

Идея автора: логика ожидания и работы хендлера **после его официального закрытия**. В
`chestor_bot` то же самое написано руками в трёх местах: `anime_router` ждёт нарезку до 60 с
прямо в хендлере (`wait_for` внутри `try` с пятью `except`); `duel/background.py` делает
`create_task` и `sleep(таймаут)` со своим набором ссылок «против сборщика мусора»;
`lottery.py` шлёт кубик, спит `animation_duration + 1` и показывает результат.

- **Зачем именно после закрытия.** Пока хендлер ждёт, он держит слот
  `max_concurrent_updates` и открытую сессию БД из мидлвари, а записанное им не
  закоммичено. Вынесенное ожидание идёт после `post_handle` (после коммита), слот и сессия
  освобождены.
- **`self.defer(fn, *args, delay=0.0)`** (и `ctx.defer` для мидлварей): записывает вызов
  async-функции, возвращает ручку `Deferred` с `.cancel()`. **`after_handle()`**: метод
  хендлера, который диспетчер запускает так же, после закрытия, с сохранённым `self`.
  Внутри это одна механика: `after_handle` это неявный `defer`.
- **Как ждёт.** Не диспетчер и не поток: на каждый вызов создаётся отдельная задача asyncio
  (`sleep(delay)`, потом функция), которую держит реестр `BackgroundTasks`. Спящая задача не
  занимает ни процессор, ни слот (объект в памяти).
- **Запуск только после успеха** (как `on_commit` в Django): если хендлер, мидлварь или
  `pre_handle` упали (даже если `on_error` хендлера ошибку обработал), записанное
  отбрасывается. Иначе бот сказал бы «напомню», а откат оставил бы базу пустой. Для этого
  `BaseRouter.propagate` теперь возвращает хендлер только при успехе, иначе `None`.
- **Чистый контекст.** Вызов идёт в новом `contextvars.Context()`: `ContextVar` сессии БД
  из мидлвари там не виден (`get()` даст `LookupError`, а не закрытую сессию). Есть `self` и
  `self.ctx` (бот, апдейт, `ctx.fsm`); БД: открыть свою.
- **Ошибки идут привычным путём:** из `after_handle` и `defer` через `owner.on_error`,
  потом `Dispatcher.on_error`; иначе только в лог.
- **Лимит `Dispatcher.max_deferred = 1000`** (отдельно от слотов апдейтов). Лишний `defer`
  даёт `DeferredLimitError` сразу в хендлере, лишний `after_handle` идёт в `on_error`.
  Защищает от бесконечного роста при спаме команды с долгим ожиданием.
- **Остановка:** `runner.drain()` (хендлеры доработали и записали свои вызовы), затем
  `BackgroundTasks.drain(shutdown_timeout)`: спящие таймеры отменяются сразу (`docker stop`
  не ждёт час), идущие вызовы дожидаются до тайм-аута, потом отменяются. Только после
  этого `on_shutdown`.
- **Границы.** Таймеры в памяти: после перезапуска пропадают; для важного («через сутки»)
  нужно своё хранилище (у `chestor_bot` это `scheduled_notifications` и `notification_ticker`
  в БД); интерфейс хранилища можно будет сделать подставным, как `Storage` у FSM. Срабатывание
  «не раньше delay», без гарантии миллисекунд. Задача на вызов, а не общий «будильник» со
  списком: проще, а для тысяч таймеров этого хватает.
- Проверено: 21 тест (порядок «после мидлварей», задержка, отмена до и после старта,
  отбрасывание при падении, ошибки, изоляция контекста, лимиты, остановка) и живой пример
  `examples/deferred_bot.py` (`/secret`, `/remind`, `/report`).

### Аргументы команд как данные: `CommandArgs` (`command_args.py`, `filter/command.py`)

Идея автора (черновик `examples/data_parsed_bot.py`): описать форму аргументов один раз,
разбор и приведение типов отдать библиотеке. Та же мысль, что у `CallbackPayload` и
`State(Model)`.

```python
class CalcArgs(CommandArgs):
    one: int
    operator: Literal["+", "-", "*", "/"]
    two: int

cmd = Command("calc", CalcArgs);  args = cmd.parse(ctx)     # CalcArgs
```

- **Модель pydantic, а не смесь аннотаций и присваиваний.** Порядок аргументов это порядок
  полей; в черновике `operator = r"..."` без аннотации выпал бы из порядка (аннотации и
  обычные атрибуты класса хранятся раздельно). Ограничения задаются штатно: `Literal`,
  `Field(pattern=...)`.
- **Не `ctx.args`, а `self.cmd.parse(self.ctx)`.** Тип `ctx.args` нельзя вывести из атрибута
  хендлера (та же причина, по которой узкий тип указывается в заголовке), а хранить
  разобранное в фильтре нельзя (он общий для параллельных апдейтов). Тот же явный приём,
  что у `TextRegexp.match` и `Payload.filter().parse`. Перегрузки `__init__` делают
  `Command` обобщённым: с моделью `parse` возвращает её, без модели `CommandCall`.
- **Фильтр совпадает по имени команды, а не по числу аргументов.** Неверные значения и
  неверное число аргументов поднимаются в `parse` как `CommandArgsError`, поэтому на любую
  ошибку ввода приходит одна и та же подсказка `exc.usage`. Иначе `/calc 2 +` получало бы
  тишину. `strict=True` возвращает прежнее поведение (`args_count`): неверные аргументы
  значат «не подходит», апдейт идёт следующему хендлеру. Старый `args_count` остался
  keyword-only; вместе с моделью он даёт `DefinitionError`.
- **`CommandArgsError(SelfrotError, ValueError)`**: `usage` (`/calc <one> <operator:
  +|-|*|/> <two>`, необязательные в `[]`, остаток с `...`), `problems` (по полям: `field`,
  `message`, `value`), `command`, `text`. Сообщения pydantic для частых случаев переведены
  («нужно целое число», «не хватает аргумента»), остальные идут как есть.
- **Необязательные аргументы:** поле со значением по умолчанию, только в конце (обязательное
  после необязательного: `DefinitionError` при объявлении класса). **`Rest`**: последнее
  поле-остаток, забирает хвост строки с сохранением пробелов.
- Проверено: 22 теста (типы, необязательные, `Rest`, префиксы и `@упоминание`, ошибки и
  подсказка, строгий режим, ошибки описания, сквозной хендлер) и pyright: `args.operator`
  выводится как `Literal[...]`, вызов с моделью и `args_count` подсвечивается в редакторе.

### Вложенное сужение: условия над ответом (`Reply[T]`, `HasReply*`, `utils/narrowing.py`)

Запрос автора (`.issues/double_types.py`): библиотека не сужает вложенные типы, поэтому для
`ctx.message.reply_to_message.user.id` приходится вручную проверять поля и делать `assert`.

- **`assert` не нужен, нужен `if`.** Проверено на pyright: `if reply and reply.user:` даёт
  `int` для `reply.user.id`, в том числе через `self.ctx.message...`, после `await` и с ранним
  `return`. Поэтому вложенное не обязано быть частью библиотеки, и в документации `if` описан
  как законный способ, а не обходной путь.
- **Настоящая дыра была в проверке, а не в типах.** Суженный тип для вложенного поля можно
  написать руками, но проверка заголовка сверяла только плоские имена: заголовок с
  `reply_to_message.user` проходил с фильтром, который смотрит лишь `reply_to_message`.
  `required_fields` теперь возвращает пути (`reply_to_message`, `reply_to_message.user`), а
  остальное не менялось: `Guarantee`, `&` (объединение), `|` (пересечение) работают с
  множеством строк как раньше. Поле считается вложенным сужением, если его тип это
  подтип типа Bot API из корня (`root_type(nested) is original`).
- **Готовые условия, но не для всех случаев.** Для самых частых есть типы и фильтры (13 полей
  в `REPLY_ATTRS`: `user`, `text`, `entities`, `caption`, `caption_entities`, `photo`,
  `animation`, `audio`, `document`, `sticker`, `video`, `video_note`, `voice`), для остального
  `if` или свой `Reply[...]`. Те же поля для самого сообщения были и раньше (`TextMessage`,
  `HasText`, ...): не хватало только уровня ответа. Глубже нечего добавлять: Telegram не
  заполняет `reply_to_message` у сообщения внутри `reply_to_message`. Имена: `HasReplyVideo`
  это «у ответа есть видео», а не `HasReplyMarkup` («у сообщения есть клавиатура»):
  схожесть случайна, так называются поля Bot API. У `CallbackQuery` и `InlineQuery` реплаев по сути нет, поэтому
  вложенное сужение сделано только для `Message`.
- **Один обобщённый тип, а не набор классов.** Сначала думали о `ReplyUserMessage`,
  `ReplyPhotoMessage`, ... как о классах. Их нельзя складывать: класс с двумя базами,
  сужающими `reply_to_message` по-разному, pyright отвергает (`define variable in incompatible
  way`), берёт первый тип, и второе условие пропадает. Пересечения типов в Python нет, поэтому
  несколько условий над ответом это один внутренний тип, собранный наследованием
  (`class PhotoCaption(PhotoMessage, CaptionMessage)`), а `Reply[PhotoCaption]` кладёт его в
  поле. `ReplyUserMessage = Reply[UserMessage]` это просто алиас. Фильтры при этом
  складываются как раньше: `HasReplyPhoto() & HasReplyCaption()` даёт оба пути.
  Два `Reply[...]` как базы pyright тоже отвергает: `Base classes are mutually incompatible`.
- **Аргумент обобщения читаем из pydantic.** `get_type_hints` для `Reply[UserMessage]` отдаёт
  неразрешённый `TypeVar`, а сам аргумент лежит в `__pydantic_generic_metadata__` (`origin`,
  `args`, `parameters`). `_resolve` подставляет его, обходя MRO, поэтому работают и
  `class Warn(TextMessage, ReplyUserMessage)`, и алиас как база. Это внутренний атрибут
  pydantic: `test_pydantic_keeps_the_generic_argument_where_we_read_it` упадёт первым, если
  устройство изменится. Весь набор проходит на pydantic 2.11.0 (нижняя граница) и 2.13.
- **Как уже не надо.** `ReplyTo[T]` без чтения метаданных проходил pyright, но проверка при
  импорте не видела аргумент: обещание `ReplyTo[TextMessage]` принималось с фильтром,
  который гарантирует только `user`. Чтобы обещание можно было проверить, аргумент читается.
- **Проверено:** 73 теста (`tests/test_nested_types.py`, сквозной в `test_examples.py`):
  пути для алиасов, комбинации, два уровня, свой вложенный тип без обобщений, фильтры по
  каждому полю и для другого вида события, `&` и `|`, все варианты заголовка (в том числе
  «раньше проходило молча»), пример `reply_bot`, тип в `selfrot tree` (`Reply[PhotoCaption]`);
  весь набор (429) на 3.11, 3.12 и 3.13; pyright на `selfrot examples scripts` без ошибок,
  причём без обещания в заголовке пример даёт ошибки `Optional` (проверка типов настоящая).
  Не проверялось: Pylance (только pyright 1.1.414).

### Скачивание файлов: `ctx.download`, `Bot.download`, `Bot.download_file`

Известное ограничение с версии 0.1.0 («нет скачивания файлов»): `Bot.get_file(file_id)`
сгенерирован из спецификации и отдаёт `File.file_path`, а дальше пользователь сам собирал
URL `https://api.telegram.org/file/bot<token>/<file_path>` и ходил в него руками.

- **Рукописный код, не генератор.** `getFile` не похож на остальные методы: нет `chat_id`/
  `message_id`, по которым генератор строит методы на объектах (`message.answer()`), и сам файл
  отдаётся отдельным HTTP GET на другой базовый URL, а не через `call()`/JSON-ответ Bot API.
  Городить в генераторе шаблон ради одного случая не стоило; `TELEGRAM_FILE_API` рядом с
  `TELEGRAM_API` (`client/telegram.py`), `AsyncSession.download()` рядом с `__call__`
  (`client/session.py`, общий `_redact()` для обоих — токен и прокси вычищаются из текста
  ошибки одинаково), `Bot.download_file`/`Bot.download` рядом с `close_session`.
- **Три слоя, а не один метод на всё.** Автор поделился опытом: единственный «умный» метод
  плохо ведёт себя, когда становится нужно что-то за его пределами. Поэтому:
  `bot.download_file(file_path)` — сырые байты по известному пути; `bot.download(file_id)` —
  `get_file` + `download_file` вместе; `ctx.download(destination)` — находит file_id сам и
  пишет на диск. Явный шаг всегда доступен, ни один уровень не прячет данные, которые дают
  соседние.
- **`ctx.download` угадывает поле, но не гадает.** У `Message` в один момент заполнено не
  больше одного из `photo`/`animation`/`audio`/`document`/`sticker`/`video`/`video_note`/
  `voice` — это факт формата Bot API, а не догадка библиотеки. Метод проверяет их по порядку
  (`_media_file_id` в `context/helpers.py`), для фото берёт самый большой размер. Работает и
  для сообщения под кнопкой callback — через тот же `_source_message()`, на котором стоят
  остальные ярлыки `ctx.*`.
- **И `reply_to_message`, если у самого сообщения медиа нет.** Упущено в первой версии: автор
  спросил «а как скачать по reply?», и оказалось, что `/save` текстом в ответ на чужое фото
  просто падал с `ContextError`, хотя пример это обещал. Частый случай («команда текстом на
  чей-то файл»), поэтому `_downloadable_file_id` теперь смотрит сначала на само сообщение, а
  если там пусто — на `message.reply_to_message` (один уровень, как у `Reply[T]`: глубже
  Telegram и не заполняет). Оба заполнены — побеждает своё сообщение: «то, что прислали
  только что» понятнее, чем «то, что процитировали», и не зависит от того, в каком порядке
  проверять поля.
- **Ничего не находит — `ContextError`.** Тот же класс, что у `ctx.answer_message` без чата:
  «действие не подходит апдейту», а не отдельная ошибка на каждый ярлык.
- **Расширение из настоящего `file_path`, а не угадыванием.** Второй промах в первой версии:
  автор запустил `download_bot` и увидел в `downloads/` файл `173` без расширения — открыть
  нечем. Гадать по виду медиа (`photo` → `.jpg`, `voice` → `.ogg`) не стали: у стикеров и видео
  формат зависит от параметров, а `File.file_path`, который и так уже приходится спрашивать у
  `getFile`, уже содержит настоящее расширение (`photos/file_1.jpg`, `voice/file_2.oga`).
  `ctx.download` теперь делает `get_file` + `download_file` сама (раньше звала `bot.download`,
  внутри которого `file_path` терялся), и если у `destination` нет `.suffix` — берёт его из
  `Path(file.file_path).suffix`. Указали своё расширение — оно не трогается: подстановка только
  когда решать пользователю нечем. `bot.download`/`bot.download_file` остаются как были: отдают
  байты, ни расширений, ни путей не решают — это работа только `ctx.download`, слоя «сделай всё
  сам». Пример `Resave` (у него только `file_id`, апдейта нет) для того же результата вызывает
  `get_file`/`download_file` сам, а не `bot.download`: без `get_file` расширение неоткуда взять.
- **Третий промах, там же: автор поправил «не только Document» — и оказался прав.** Я сказал
  «`file_name` есть только у `Document`», не проверив. На деле поле есть ещё у `Animation`,
  `Audio` и `Video` (у всех четырёх Telegram присылает `Optional[str] file_name` — как файл
  назывался у отправителя); у `Sticker`, `VideoNote`, `Voice`, `PhotoSize` его нет вообще —
  проверено `grep -n file_name selfrot/types/generated.py`, а не по памяти. `_media_file_id`
  теперь отдаёт `(file_id, оригинальное_имя)`, явными ветками по типу (без `getattr` — так
  pyright по-прежнему точно знает, у какого типа какие поля, а не молчит через `Any`).
  `ctx.download` при подстановке расширения сначала берёт суффикс из оригинального имени, и
  только если его нет — из `file_path`: имя, которое дал отправитель, точнее внутреннего пути
  Telegram. `Bot.download`/`Bot.download_file` это не касается — они как были, только байты.
  Сам базовый выбор имени файла (`str(message_id)` в примере `Save`) остался как был:
  оригинальные имена не гарантированно уникальны между разными сообщениями, а `message_id` —
  да, так что автоматически подставлять его вместо `message_id` значило бы рисковать
  перезаписью чужого файла. Спросил у автора, а не решил сам — и это привело к следующему
  пункту.
- **`overwrite`: явный параметр, а не поведение по умолчанию.** Автор явно попросил дать
  выбор — перезаписывать или плодить копии `(1)`, `(2)`, ... — раз уж свои имена не гарантируют
  уникальность (`/save отпуск` дважды подряд про разные файлы). `overwrite: bool = True` —
  ключевое слово, по умолчанию поведение как раньше (молча заменяет), `overwrite=False` не
  трогает существующий файл и подбирает первое свободное имя.
  Реализация — не «проверить exists(), потом записать» (гонка: апдейты обрабатываются
  параллельно, `max_concurrent_updates` по умолчанию 100, два могли бы одновременно решить,
  что имя свободно), а `open(candidate, "xb")` в цикле: атомарное «создать, если файла ещё
  нет» на уровне ОС, `FileExistsError` — пробуем следующий номер. `_write_new` в
  `context.py`, вызывается через `asyncio.to_thread`, как и запись при `overwrite=True`.
  В примере `overwrite=False` включается только для `/save <имя>` (`SaveArgs.name: Rest`):
  вариант по `message_id` в столкновении не нуждается, поэтому там `overwrite=True`
  (по умолчанию, но указано явно в примере ради наглядности).
- **`ctx.download` не создаёт папки.** `destination` целиком на пользователе: если её
  родительской директории нет, `FileNotFoundError` при записи, а не тихое создание дерева
  папок. Явное поведение, а не удобство ценой неожиданностей.
- **Возвращает `bytes`, а не пишет сам.** `Bot.download`/`Bot.download_file` симметричны
  `InputFile.read() -> bytes` на стороне загрузки: сохранение на диск — `Path(...).
  write_bytes(data)`, одна строка, никакой обёртки не нужно. `ctx.download` берёт это на себя
  только для частого случая («сохранить файл апдейта»), через `asyncio.to_thread` — как и
  `InputFile.from_path` не блокирует цикл событий на чтении.
- **`FileNotAvailableError`, не голый `ValueError`.** `File.file_path` в спецификации формально
  `Optional` (редкий случай, Telegram документирует его так и для успешного `getFile`), а
  каждая ошибка библиотеки — свой класс от `SelfrotError`, ни одна не бросается напрямую.
- **Неверный `file_id` — это `TelegramAPIError`, не наша ошибка.** Он идёт через обычный
  `get_file()`/`call()` и получает обычную обработку ответа Bot API (`TelegramBadRequest` и
  т. п.), `FileNotAvailableError` — только для настоящего «`getFile` ответил ok, но без пути».
- Проверено: 35 тестов — 33 в `tests/test_download.py` (скачивание байт по пути и по id, 404 →
  `TelegramAPIError`, обрыв → `TelegramNetworkError` без токена в тексте, таймаут →
  `TelegramTimeout`, прокси не течёт в ошибку, `file_path=None` → `FileNotAvailableError`,
  каждое поле медиа по отдельности, самый большой размер фото, апдейт без медиа нигде →
  `ContextError`, медиа только в reply, своё сообщение сильнее reply, callback с медиа в
  сообщении под кнопкой, отсутствие родительской папки → `FileNotFoundError`, расширение
  дописывается из `file_path`, заданное не трогается, у animation/audio/document/video
  расширение из `file_name` побеждает `file_path`, у фото/стикера/кружка/голосового —
  всегда `file_path`, `overwrite=True` заменяет молча, `overwrite=False` подбирает
  `" (1)"`, `" (2)"`, ... и не трогает существующий файл) и 2 в `test_examples.py` (пример в
  реестре, сквозной сценарий `download_bot` — включая `/save имя` дважды подряд); весь набор
  (501) на 3.11, 3.12, 3.13 и pydantic
  2.11.0; pyright на `selfrot examples scripts` и на самом
  тестовом файле без ошибок (заодно поправлен старый баг типизации `AsyncIterator`-фикстуры —
  тот же, что уже был в `test_transport.py`, но CI его не ловит: pyright гоняется только по
  `selfrot examples scripts`, не по `tests/`).

### Несколько триггеров у одной команды: `AnyCommand` (`filter/command.py`)

Запрос автора (`.issues/commands.py`): команда перевода должна вызываться и как `/transfer`,
и как «перевести»/«подать»/«кинуть» без префикса, с одной моделью аргументов. Обходной путь
(класс-обёртка с кортежем `Command`, `first | second | ...` для фильтра и собственный
`parse`, перебирающий команды заново) работал, но каждому проекту пришлось бы писать его
заново. Разобрано на прогоне: ошибки не было, был недостаток API.

- **Отдельный фильтр-группа, а не расширение `Command`.** Список имён в одном `Command` не
  решает смешанные префиксы (`/transfer` рядом с «перевести» без префикса), а `Command | Command`
  возвращает `OrFilter`, который не помнит, какая ветка сработала. Поэтому `AnyCommand(*commands)`
  хранит сами `Command` и умеет `find(ctx)` (сработавшая), `parse(ctx)` (её аргументы), `check`.
- **Явно, а не через `|`.** Можно было бы переопределить `Command.__or__` так, чтобы он
  возвращал группу, но тип результата стал бы зависеть от операндов: `Command | Text`
  вернул бы одно, `Command | Command` другое. Это как раз та неявность, которой мы избегаем.
  Обычный `|` остался как был.
- **Тот же `usage`.** `CommandArgsError` создаёт сработавшая команда, поэтому подсказка
  пишет то слово, которым позвали (`перевести <to> <amount>`), а не первое из списка.
- **Разные модели у разных слов.** `TParsed` в `Command` сделан ковариантным, и pyright выводит
  для `AnyCommand(Command("a", A), Command("b", B))` тип `AnyCommand[A | B]`, а `match` по
  результату сужает его. Проверено: с неизменяемым `TParsed` `Command[B]` рядом с `Command[A]`
  не принимается. Для остального кода ковариантность безопасна: `TParsed` встречается только
  в возвращаемом значении `parse`.
- **`Command.matches(ctx)`: `check` без `await`.** У `check` асинхронная сигнатура только
  ради общего интерфейса фильтров, а разбирает он одну строку. Синхронный `matches` даёт
  синхронный `AnyCommand.parse`, как у `Command.parse`, без обращения к приватному `_parse`.
- **Разбор не кэшируется.** `parse` заново разбирает строку после `check`: это микросекунды,
  а положить результат в фильтр нельзя (общий для параллельных апдейтов), в `ctx` значило
  бы скрытое состояние.
- **`selfrot check`:** два `AnyCommand` с одинаковым `repr` считаются одним фильтром,
  только если попарно совпадают команды, включая сами классы моделей (как у одиночного `Command`).
- **`selfrot tree`:** группа печатается в несколько строк, как в коде (`AnyCommand(`, по строке на
  команду, `)`), в том числе внутри `&`, `|` и `~`. Ветки дерева слева остаются, пока ниже есть
  хендлеры, пометка «недостижим» стоит после закрывающей скобки. Раскладывает только `tree`
  (`_pretty` в `cli/tree.py`), а `repr` фильтра остаётся однострочным: по нему `selfrot check`
  сравнивает фильтры и печатает причину.
- **Заодно почищен вывод для длинных цепочек `&`/`|`.** `AnyCommand` с несколькими триггерами
  ведёт к длинным `Command(...) | Command(...) | ...`, а `&`/`|` левоассоциативны, поэтому без
  этого печаталось бы `((((a | b) | c) | d) | e)`. `chain()` в `cli/analysis.py` разбирает такую
  цепочку в плоский список операндов (останавливаясь на другом операторе: `a & (b | c)` даёт
  `[a, (b | c)]`), а `flat_repr()` там же — однострочная версия без вложенных скобок, ею теперь
  пользуется и причина «недостижим» в `tree`, и в `check`. `tree._combine()` поверх того же
  `chain()` решает, уместилась ли строка (`_MAX_INLINE = 72`, без учёта отступа строки в
  дереве): короткая цепочка остаётся в одну строку, как раньше, длинная — по операнду на
  строку, вложенные блоки (например, `AnyCommand` внутри `&`) сдвигаются дальше. Ради этого
  общее правило для `AndFilter`/`OrFilter` внутри `&`/`|` сменилось: раньше первый операнд
  всегда лип к открывающей скобке (`(FromUser(7) & AnyCommand(`), теперь оба операнда всегда
  на отдельных строках, если хоть один из них многострочный — так однообразнее и без частных
  случаев.
- Проверено: 44 теста (`tests/test_any_command.py` и четырнадцать в `test_cli_tree.py`): все
  триггеры, порядок, `strict` у каждой команды, разные модели, usage сработавшего слова,
  сквозной хендлер, гарантия `TextMessage` в заголовке, `&` с другим фильтром, разбор и плоский
  repr цепочки, короткая цепочка в одну строку, длинная — по операнду на строку, причина
  «недостижим» без вложенных скобок; pyright на `selfrot examples scripts` без ошибок, весь
  набор (393) на 3.11, 3.12, 3.13 и на pydantic 2.11.0 (нижняя граница).

### Инлайн-клавиатуры и данные кнопок (`keyboard.py`, `callback_data.py`)

У `chestor_bot` клавиатуры собираются вручную (`InlineKeyboardMarkup`), а
`callback_data` упаковывается строкой и разбирается руками в пяти местах
(`duel:<id>:<action>:<uid>`, `quiz_answer_<id>_<option>`, `<prefix><count>_<current>_<view>`
и т. д.), плюс `parse_duel_callback_payload` с `VALID_ACTIONS`. Это рутина, которую
берёт на себя библиотека. Пример: `examples/keyboards_bot.py`.

```python
class Duel(CallbackPayload, prefix="duel"):
    duel_id: int
    action: Literal["consent_target", "fora_serious"]
    expected_id: int

kb = InlineKeyboard(width=2).button("Принять", Duel(duel_id=1, action="consent_target", expected_id=5))
await msg.reply("Вызов!", reply_markup=kb.markup())      # callback_data == "duel:1:consent_target:5"

class Consent(CallbackQueryHandler[AppContext[DataCallbackQuery]]):
    duel = Duel.filter(action="consent_target")
    query = duel
    async def handle(self):
        data = self.duel.parse(self.ctx)                 # Duel: duel_id уже int
```

- **`CallbackPayload`** (pydantic-модель, `prefix=` обязателен, `sep=":"` по умолчанию):
  поля упаковываются в порядке объявления. Допустимы `str`, `int`, `bool`, `Enum`,
  `Literal`, `Optional` (`None` — пустое поле). `pack()` / `unpack()` / `try_unpack()`.
  Разбор проверяет префикс, число и типы полей (`Literal` заменяет `VALID_ACTIONS`).
- **Лимиты Telegram проверяются заранее**, а не ответом 400 при отправке:
  `callback_data` до 64 **байт** (кириллица — 2 байта; `CallbackDataError` с размером),
  разделитель внутри значения, ровно один вид кнопки, до 8 кнопок в ряду и 100 всего.
- **`Payload.filter(**equals)`** — фильтр по данным кнопки (гарантирует
  `DataCallbackQuery`); поля-условия проверяются при создании (опечатка → `DefinitionError`).
  Комбинируется как остальные: `Duel.filter(action="a") | Duel.filter(action="b")`.
  Разобранный объект в фильтре не хранится (он общий для апдейтов): `parse(ctx)` в
  хендлере, как `TextRegexp.match(ctx)`. Pyright выводит тип `Duel`.
- **`InlineKeyboard(width=N)`**: `button()` кладёт кнопки по `N` в ряд (замена
  `builder.adjust(N)`), `row(*buttons)` — отдельный ряд, `markup()` отдаёт
  `InlineKeyboardMarkup`. `button(text, data | Payload, url=..., **fields)` принимает
  и остальные поля (`web_app=`, `style="success"`), опечатки в именах — `KeyboardError`.
  Пустая клавиатура допустима (убирает кнопки у сообщения).
- **Проверка «нажал тот, для кого кнопка»: `.pressed_by("поле")`.** В группе кнопку
  видят все, а нажать может только тот, чей id зашит в payload (`expected_id`,
  `invoker_id`). Фильтр пропускает только нажатие владельца; чужое не совпадает, поэтому
  следующим по списку хендлером его ловят и отвечают (первый подошедший хендлер
  забирает апдейт):

  ```python
  class Consent(CallbackQueryHandler[...]):
      duel = Duel.filter(action="accept").pressed_by("expected_id")
      query = duel
      async def handle(self): data = self.duel.parse(self.ctx); ...

  class NotForYou(CallbackQueryHandler[...]):          # ниже по списку handlers
      query = Duel.filter(action="accept")
      async def handle(self): await self.ctx.callback_query.answer("Не для тебя", show_alert=True)
  ```

  Без второго хендлера чужое нажатие останется без ответа (у кнопки крутится
  индикатор), поэтому проверка не молчаливая по умолчанию, а явная. Возвращает
  копию, исходный фильтр не меняется; поле проверяется при создании.
- **`FromUser(*ids)` (`filter/user.py`)** — общий фильтр по отправителю: автор
  сообщения, нажавший кнопку, участник, чей статус изменился (то, что `ctx.user`
  отдаёт для любого вида апдейта). Подходит любому виду обработчика, у события без
  пользователя (пост канала) не совпадает: `FromUser(*ADMIN_IDS) & Command("ban")`,
  `~FromUser(*BANNED)`. Заменяет `CreatorMiddleware` там, где нужна не блокировка
  всего роутера, а условие на один хендлер.
- Нет reply-клавиатур (`ReplyKeyboardMarkup`): в `chestor_bot` они не используются.
- **Найденная ошибка, исправлена в генераторе:** `CallbackQuery.message` — это
  `MaybeInaccessibleMessage`, а у `InaccessibleMessage` те же поля, что у `Message`,
  поэтому разбор *всегда* возвращал `Message`, и `isinstance(msg, Message)` не
  отличал недоступное сообщение (старше 48 часов) от обычного. Теперь дискриминатор
  `date == 0`. Правка сообщения под кнопкой без `isinstance` уже есть:
  `ctx.edit_message_text("...", reply_markup=...)` берёт чат и id из апдейта и
  работает даже для недоступного сообщения.

### Фильтры статуса участника (`filter/member.py`)

`chat_member` и `my_chat_member` приходят как `ChatMemberUpdated` с
`old_chat_member` и `new_chat_member`; у каждого `status`: `creator`,
`administrator`, `member`, `restricted`, `left`, `kicked`. Сами по себе они не
говорят «вошёл» или «вышел», надо сравнить до и после.

- `MemberJoined()` — раньше не в чате, теперь в чате (вошёл, добавлен, заявка
  одобрена); `MemberLeft()` — наоборот (вышел, удалён, **заблокирован**). Это
  `JOIN_TRANSITION` и `LEAVE_TRANSITION` из aiogram.
- «В чате» = `creator`/`administrator`/`member`, а у `restricted` решает поле
  `is_member`: ограниченный участник может как остаться в чате (заглушили), так и
  быть вне его. Вошёл и сразу ограничен — это вход, заглушили уже вошедшего — нет.
- `ChatMemberTransition(before=..., after=...)` — переход между конкретными
  статусами (строка, множество или `None` = любой): повышение
  (`before="member", after="administrator"`), бан (`after="kicked"`). Опечатка в
  названии статуса даёт `DefinitionError` при создании фильтра.
- Работают и в `MyChatMemberHandler` (статус самого бота), и в `ChatMemberHandler`
  (других), потому что читают `ctx.event`. В `MessageHandler` их поставить нельзя:
  заголовок сверяется при создании класса (`DefinitionError`). Пример:
  `examples/chat_members.py` (порт `chat_member_update_routers`).

### Значения по умолчанию: `BotDefaults` (`client/defaults.py`)

Аналог `DefaultBotProperties` из aiogram. В `chestor_bot` реально нужен один
параметр, `link_preview_is_disabled=True`, а `parse_mode="HTML"` там передаётся
вручную в 17 местах.

```python
class MyBot(Bot):
    defaults = BotDefaults(
        parse_mode="HTML",
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
```

- **Явно и типизированно:** атрибут класса `Bot` (как таймауты и `proxy`), поля
  `parse_mode`, `link_preview_options`, `disable_notification`, `protect_content`,
  `show_caption_above_media`. Вместо плоских `link_preview_is_disabled`,
  `link_preview_prefer_small_media`... из aiogram — сам объект `LinkPreviewOptions`,
  без пересборки.
- **Подстановка в `Bot.call`, до сериализации:** в поле, которое вызов оставил
  `None`, кладётся умолчание. Работает и для ярлыков (`ctx.answer_message`), и для
  прямых вызовов. Исходный метод не меняется (копия).
- **Вложенное тоже:** `InputMedia*` в `send_media_group`, `InputTextMessageContent` в
  результатах `answer_inline_query` (по имени поля, рекурсивно по спискам, моделям и
  методам-датаклассам). Иначе `parse_mode="HTML"` не действовал бы на подписи
  альбома.
- **Явное сильнее умолчания:** `link_preview_options` заменяется целиком, а
  `disable_notification=False` перекрывает `True`.
- **Ограничение: `parse_mode` на один вызов не отключить.** Значения «без разметки»
  у Telegram нет (а отличить «не задано» от «нет» без sentinel в сигнатурах всех
  185 методов нельзя). Для такого вызова текст экранируют. Если `parse_mode` по
  умолчанию задан, а в тексте сырой `<`, будет `400 can't parse entities` (как и в
  aiogram). Не покрыто: `text_parse_mode`, `quote_parse_mode`,
  `allow_sending_without_reply` (у них другие имена/семантика).
- **Найденное попутно, исправлено в генераторе:** у входных типов `InputMedia*`,
  `InlineQueryResult*`, `RichText*` поле `type` было обязательным `str`, и
  `InputMediaPhoto(media="id")` не создавался без `type="photo"`. Причина: в
  описании «must be photo» без кавычек, а у `InlineQueryResultPhoto` и `…CachedPhoto`
  одинаковое значение, из-за чего дискриминатор объединения не собирался. Теперь
  единственное значение — `Literal["photo"]` с умолчанием у каждого типа отдельно
  (175 полей вместо 92), независимо от дискриминатора объединения.

### Вебхуки и жизненный цикл (`dispatcher/webhook.py`, `dispatcher.py`)

Сделано под реальный `chestor_bot`: прод на VPS, aiohttp за nginx (порт 8999,
`127.0.0.1` наружу), в `__main__` те же воркеры (`video_worker`, `notification_ticker`)
и один код для DEV (поллинг) и PROD (вебхук). Пример: `examples/webhook_bot.py`.

```python
dp.start_webhook(url="https://chestor.site/webhook/x", secret_token=..., host="0.0.0.0", port=8999)
dp.start_polling()
```

- **Общий вход `feed_update(update)`** (ждёт слот) и `try_feed_update(update) -> bool`
  (не ждёт). Поллинг и вебхук отдают апдейты туда, а `UpdateRunner` создаётся в
  `__init__`. `feed_update` можно звать и из своего FastAPI/aiohttp-приложения.
- **`on_startup()` / `on_shutdown()`** — методы диспетчера (как `on_error`,
  `ordering_key`), а не регистрации. Старт: `getMe` (токен проверен) →
  `on_startup` → приём. Стоп: перестать принимать → дождаться хендлеров
  (`drain`) → `on_shutdown` → закрыть сессию. `on_shutdown` зовётся, если
  `on_startup` был начат, даже если упал: останавливать нужно то, что могло и не
  запуститься. Аналог `dp.startup`/`try…finally` в `__main__` прода.
- **Сервер (`WebhookApp`) поверх `aiohttp.web`, без новых зависимостей.** Путь
  берётся из `url`. TLS терминирует прокси, сервер слушает обычный HTTP
  (`host="127.0.0.1"` по умолчанию; в контейнере нужен `"0.0.0.0"`).
  `access_log=None`: в строке запроса лежит путь, а у прода в нём токен бота.
- **`secret_token` обязателен** (`[A-Za-z0-9_-]{1,256}`, иначе `ConfigError`),
  сравнение через `hmac.compare_digest` (не-ASCII в заголовке — 403, а не 500). У
  прода секретом служит путь `/webhook/<BOT_TOKEN>`, то есть токен бота попадает в
  логи nginx и в `logs.log`. Заголовок секрета это исправляет: при переносе путь
  можно сделать любым.
- **Ответы:** 403 (секрет), 400 (не JSON или не `Update`), 404/405 (путь/метод), 200,
  503 + `Retry-After` (очередь переполнена: Telegram повторит; апдейт при этом не
  запоминается принятым). 200 отдаётся сразу после постановки в очередь, а не
  после обработки, иначе долгий хендлер выглядел бы для Telegram провалом.
- **Дедупликация по `update_id`** (последние 1000): Telegram повторяет доставку при
  сбое, а у `getUpdates` есть `offset`, у вебхука его нет.
- **Если порядок включён явно, при вебхуке он слабее, чем при поллинге.** Telegram шлёт
  до `max_connections` (по умолчанию 40) запросов параллельно, апдейты одного чата
  могут прийти по разным соединениям в другом порядке; `ordering_key` сохраняет только
  порядок прибытия. Строгий порядок — `max_connections=1` (ценой пропускной
  способности). Повтор после 503 тоже может прийти позже следующего апдейта чата.
- **`start_polling` / `start_webhook` ловят SIGINT и SIGTERM:** сигнал отменяет главную
  задачу, а её `finally` (drain, `on_shutdown`, сессия) отрабатывает штатно. Раньше
  `docker stop` (SIGTERM) убивал процесс посреди хендлеров. Второй сигнал во время
  остановки прерывает её.
- **`setWebhook` после запуска сервера**: `allowed_updates` считается из дерева
  роутеров (у прода он записан вручную), `drop_pending_updates` и `max_connections`
  — параметры. Вебхук при остановке не снимается: апдейты за время рестарта
  Telegram хранит и доставит (прод при старте сбрасывает их через
  `drop_pending_updates`).
- **Поллинг при установленном вебхуке**: `getUpdates` отвечает 409, поллинг
  повторяет с паузой. Библиотека вебхук сама не снимает: это делает приложение в
  `on_startup` (`await self.api.delete_webhook(...)`), как `main` прода в DEV.
- **Прокси**: `Bot.proxy = "http://host:port"` (у прода `AiohttpSession(proxy=...)`),
  адрес прокси из текста ошибок вырезается.
- Проверено на локальном фейк-сервере Telegram и настоящем сервере вебхука: 403/400/
  404/405/200, дедупликация, 503 и повтор после него, порядок старта (сервер слушает
  до `setWebhook`), остановка (хендлер доработал до `on_shutdown`, порт свободен),
  SIGTERM. С настоящим Telegram не проверялось (нужен публичный HTTPS).
- **Не покрыто, а `chestor_bot` это использует:** настройки по умолчанию для бота
  (`DefaultBotProperties(link_preview_is_disabled=True)`): у нас каждый вызов
  сам задаёт `link_preview_options`/`parse_mode`; `dp.update.middleware` (мидлвари
  на весь апдейт, у нас диспетчерские); DI-контейнер и `wire`.

### Параллельная обработка (`dispatcher/runner.py`, `dispatcher.py`)

Раньше `polling()` делал `await create_task(...)` на каждый апдейт, то есть шёл
по очереди: один медленный хендлер (БД, внешний API) задерживал весь бот. Теперь
апдейты идут параллельно, но не как попало.

- **По умолчанию порядка нет: каждый апдейт независим, как в aiogram.** Метод
  `ordering_key(ctx)` возвращает `None`. Порядок включается явно: апдейты с одним
  ключом идут строго друг за другом, с разными — параллельно.

  ```python
  class Root(BaseDispatcher[...]):
      def ordering_key(self, ctx):
          return order_by_chat(ctx)      # или order_by_user(ctx), или свой ключ
  ```

  Готовые ключи: `order_by_chat` (id чата, без чата — пользователь) и
  `order_by_user`. **Почему не наоборот** (сначала стоял порядок по чату): он даёт
  head-of-line blocking. Долгий хендлер (`/anime` у `chestor_bot` ждёт ffmpeg до 60 с)
  задерживает все остальные апдейты чата, в группе — всех участников, а защита
  `_active_cut_users` («у тебя уже есть нарезка»), рассчитанная на параллельность,
  молча перестаёт работать. «Бот завис» заметнее и хуже редкой гонки; гонки за важные
  данные (баланс) у прода закрыты на уровне приложения (тесты `race_condition`),
  а за несущественные (имя пользователя) — не проблема. Порядок нужен там, где хендлеры
  быстрые, а последовательность значима (диалоги, FSM).
- **Лимит одновременных: `max_concurrent_updates = 100`.** Когда все слоты заняты,
  `polling()` перестаёт забирать апдейты (Telegram их хранит), поэтому задачи не
  копятся без границы. `1` — прежнее поведение, строго по очереди.
- **Остановка (`shutdown_timeout = 10` с):** начатым хендлерам дают закончить,
  оставшихся отменяют, и их `post_handle(exc)` получает `CancelledError` (сессия БД
  откатывается, а не течёт).
- Ошибка одного хендлера логируется и не задевает остальных; слот при этом
  освобождается. Упавший апдейт не блокирует следующие того же чата.
- Планировщик — отдельный `UpdateRunner`: ссылки на задачи хранит сам (иначе
  сборщик мусора может убить задачу в середине хендлера), ошибок хендлеров не
  обрабатывает.
- **Гарантия доставки — «не более одного раза»**: `offset` двигается сразу при
  получении, до обработки. Если процесс убить, необработанные апдейты в работе
  потеряются (раньше окно было в один апдейт, теперь до `max_concurrent_updates`).
  Для RPG-бота, где апдейт — действие игрока, это стоит помнить при деплое: остановка
  по Ctrl+C/SIGINT дожидается хендлеров, `kill -9` — нет.
- Что это требует от кода пользователя: всё, что живёт на уровне диспетчера
  (сервисы, кеши), должно быть безопасно при параллельном доступе; данные апдейта
  живут в `ctx`, а хендлер и мидлвари создаются заново на каждый апдейт.
- Проверено: юнит-тесты `UpdateRunner` (параллельность, порядок ключа, лимит и
  backpressure, освобождение слотов после ошибок, drain, отмена ожидающего) и
  сквозной поллинг на локальном фейк-сервере (порядок в чате, параллельность
  чатов, `max_concurrent_updates = 1`, `ordering_key → None`, остановка с
  зависшим хендлером).

### 4. Клавиатуры и медиа

- `InlineKeyboardMarkup`/`ReplyKeyboardMarkup` как билдеры (аналог
  `InlineKeyboardBuilder` из aiogram), не голые dict.
- `sendPhoto`/`sendVideo`/`sendDocument`/`editMessage*`/
  `answerCallbackQuery` — реализовать по мере необходимости, не всё
  Bot API сразу.

### 5. Диспетчер / поллинг

- Баги диспетчера (пп. 1-3, 5 аудита) — **исправлены**, см. выше.
- Апдейт забирает первый подошедший хендлер (по порядку в `handlers`), дальше
  диспетчер не идёт. Поэтому запасной хендлер без `args_count` можно ставить
  ниже точного. Сквозные вещи (подсчёт, логи) — в мидлварях, не в хендлерах.
- Контекст апдейта больше не хранится в `self.ctx` диспетчера: он создаётся
  в `polling()` и передаётся параметром (`propagate(ctx)`). Диспетчер держит только app-lifetime сервисы, так
  что параллельная обработка апдейтов не затрёт чужой контекст (см. «Параллельная обработка»).
- Long polling и переживание сбоев сети реализованы, см. «Сеть».

### Вне ядра библиотеки (сознательно)

- DI-контейнер, работа с БД — это ответственность конкретного бота
  (как в `chestor_bot` через `dependency-injector`+SQLAlchemy), библиотека
  не должна на это завязываться.
- Webhook-режим — возможно later, не блокер для переноса `chestor_bot`
  (он и сейчас, вероятно, на поллинге или его несложно оставить так).

## Открытые вопросы

Требуют решения до реализации соответствующей части — фиксировать здесь
по мере ответов:

- [x] Синтаксис фильтров: принцип решён — **никакого magic** (это
      касается и `F`-подобных прокси-объектов из aiogram, и
      magic-прокидывания данных из middleware в хендлер через kwargs;
      именно вторую проблему в aiogram и решает явный `Context`, и
      фильтры не должны заводить новый magic взамен старого). Ориентир —
      фильтры grammY, но не копия, а попытка сделать лучше. Решено: классы
      с `check()` + комбинаторы `&`/`|`/`~` (см. «Комбинаторы фильтров»).
      Не решено: фильтры с параметрами из БД/состояния (FSM).
- [x] Router — регистрация: атрибуты класса, `register_router`,
      `register_routers()`, `auto_connect` (см. «Router» выше).
- [x] FSM: часть ядра, типизированная (см. «FSM: состояния диалогов»).
- [x] Вебхуки нужны: прод на них (VPS), см. «Вебхуки и жизненный цикл».
- [x] Ошибки в хендлерах: `on_error` на хендлере и диспетчере, см. «Ошибки хендлеров».

## Статус порта `chestor_bot`

Сверка по импортам aiogram в `src` (197 файлов) и по реальным выражениям.

**Покрыто библиотекой:**

| У прода | У нас |
|---|---|
| `Message`, `CallbackQuery`, `Router`, `Bot`, `Update` | типы, роутеры, `Bot` |
| `Command`, `CommandObject`, `CommandStart`, `or_f` | `Command` (+`parse`), `\|` |
| `F.text.lower() == "бот"` (14) | `Text("бот", ignore_case=True)` |
| `F.text.regexp(...)` (4), `F.data.startswith("duel:")` | `TextRegexp`, `CallbackDataStartswith` |
| свой `Filter` (4), `BaseMiddleware` (8) | `BaseFilter`, `BaseMiddleware` (`pre_handle`/`post_handle`) |
| `dp.update.middleware`, `router.message.middleware` | мидлвари диспетчера и роутера |
| `TelegramAPIError`/`BadRequest`/`Forbidden` | те же имена без `Error` (`TelegramForbidden`) |
| `router.errors()` / `ErrorEvent` | `on_error` |
| `DefaultBotProperties`, `AiohttpSession(proxy=)` | `Bot.defaults`, `Bot.proxy` |
| `SimpleRequestHandler`, `setup_application`, `dp.startup` | `start_webhook`, `on_startup`/`on_shutdown` |
| `FSInputFile`, `BufferedInputFile` | `InputFile.from_path`, `InputFile(bytes)` |
| `InputRichMessage` и блоки (5 файлов) | сгенерированы из спеки (Bot API 10.3) |
| `message.answer/reply/reply_video/reply_animation` (35) | `ctx.answer_message`, `ctx.reply_animation`, ... |

**Не покрыто, в порядке важности:**

1. ~~`ChatMemberUpdatedFilter(JOIN/LEAVE_TRANSITION)`~~ — сделано: `MemberJoined`,
   `MemberLeft`, `ChatMemberTransition`.
2. ~~Методы на самих сообщениях~~ — сделано: `sent.edit_text()`, `sent.delete()`,
   `callback.answer()`, `event.answer()` и остальные.
3. ~~FSM~~ и ~~`InlineKeyboardBuilder`~~ — сделаны (`selfrot.fsm`, `InlineKeyboard`, `CallbackPayload`).
4. **Тесты**: у `chestor_bot` pytest с `race_condition`; у библиотеки нет утилиты для
   прогона `Update` через диспетчер с фейковым `Bot` (все проверки этой сессии
   делались скриптами со скрытым фейк-сервером).
5. Не проверялось с настоящим Telegram: вебхуки (нужен публичный HTTPS), `getUpdates`
   long polling под нагрузкой, `Bot.defaults` на живом API.

**Исправлено при этой сверке:** `ctx.edit_message_text(text=..., message_id=...)`
слал запрос без `chat_id` (когда задан только `message_id`); теперь чат берётся из
апдейта. Проверены все способы адресации: только `message_id`, сообщение апдейта,
всё явно, `inline_message_id`, callback из inline-сообщения.

## Roadmap

1. ~~Пофиксить баги диспетчера~~ — готово.
2. ~~Router + Filters~~ — готово.
3. ~~Типизация Context по типу апдейта~~ — готово.
4. ~~FSM~~ — сделано.
5. ~~Клавиатуры, `CallbackQuery`/`InlineQuery` handlers, ответы на них~~ — типы и
   методы сгенерированы; нет `InlineKeyboardBuilder`.
6. ~~Медиа-методы~~ — сгенерированы; `attach://` для альбомов не нужен `chestor_bot`.
7. ~~Ревизия pydantic-моделей~~ — типы сгенерированы из спеки.
8. ~~Фильтры переходов `ChatMember` (JOIN/LEAVE)~~ — готово.
9. Черновой перенос простого куска `chestor_bot` (например, один роутер) как проверка
   архитектуры на реальном коде — **следующий шаг**.
