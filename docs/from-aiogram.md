# Отличия от aiogram

Если вы писали на aiogram 3, здесь много знакомого: роутеры, мидлвари, фильтры, FSM,
типизированные данные кнопок, `message.answer()`. Главное отличие в подходе: **aiogram
опирается на функции и неявную передачу аргументов, selfrotgram на классы и явный `ctx`.**

> aiogram старше, больше и проверен тысячами ботов; у него есть экосистема (например,
> `aiogram-dialog`) и сообщество. selfrotgram молодая библиотека, её ценность в другом
> подходе к типам, а не в охвате. Раздел «Чего здесь нет» ниже честный.

## Сравнение по задачам

| Задача | aiogram 3 | selfrotgram |
|---|---|---|
| Хендлер | функция с декоратором `@router.message(...)` | класс `MessageHandler` с `query = <фильтр>` и методом `handle()` |
| Что получает хендлер | аргументы по имени и типу: `message`, `state`, `bot`, свои сервисы (`dp["key"]`, `Provide[...]`) | всё через `self.ctx`: `ctx.message`, `ctx.bot`, `ctx.fsm`, поля вашего контекста |
| Аргументы команды | `CommandObject.args`: одна строка, разбор и проверка вручную | `CommandArgs`: форма аргументов моделью, `cmd.parse(ctx)` даёт объект с типами, `CommandArgsError` с подсказкой |
| Отложенные действия | вручную `asyncio.create_task(...)` и `sleep` (ссылки на задачи, лимит, остановка на вас) | `self.defer(fn, delay=...)`, `after_handle()`: после закрытия хендлера и мидлварей, с лимитом, ошибками в `on_error` и штатной остановкой |
| Фильтры | `F.text == "x"`, `Command()`, `Filter`-классы | классы: `Text("x")`, `Command("x")`, `HasText()`, свои через `BaseFilter.check()` |
| Комбинация фильтров | `and_f`, `or_f`, `&` `\|` `~` у `F` | `&`, `\|`, `~` у любых фильтров |
| `message.text` может быть `None` | проверка вручную | фильтр `HasText()` и тип `TextMessage` в заголовке: `text` всегда `str` |
| Согласованность фильтра и типов | не проверяется | проверяется при импорте (`DefinitionError`) |
| Мидлварь | `__call__(handler, event, data)`, данные кладут в словарь `data` | `pre_handle()` и `post_handle(exc)`, данные через `ctx` или `ContextVar` |
| Запретить дальше | не вызвать `handler(event, data)` | вернуть `False` из `pre_handle` |
| Ошибки | `@router.errors()` | `on_error(exc)` на хендлере, потом `on_error(ctx, exc)` на диспетчере |
| Данные кнопок | `class X(CallbackData, prefix="x")`, `X.filter(F.action == "a")`, `callback_data: X` | `class X(CallbackPayload, prefix="x")`, `X.filter(action="a")`, `self.filter.parse(self.ctx)` |
| «Нажать может только владелец» | вручную в хендлере | `.pressed_by("owner_id")` у фильтра |
| Клавиатура | `InlineKeyboardBuilder`, `.adjust(2)`, `.as_markup()` | `InlineKeyboard(width=2)`, `.button()`, `.row()`, `.markup()`; лимиты Telegram проверяются заранее |
| FSM | `StatesGroup`, `State()`, `FSMContext` (`get_data()` возвращает `dict`) | `States`, `State(Model)`, `ctx.fsm`; данные состояния это модель pydantic с типами |
| Методы на объектах | `message.answer()`, `sent.edit_text()` | так же |
| Значения по умолчанию | `Bot(token, default=DefaultBotProperties(...))` | `class MyBot(Bot): defaults = BotDefaults(...)` |
| Запуск | `await dp.start_polling(bot)` | `Dispatcher(token=...).start_polling()` |
| Вебхук | `SimpleRequestHandler` и `web.Application` вручную | `dp.start_webhook(url=..., secret_token=...)` |
| Параллельность | каждый апдейт отдельной задачей | так же, лимит `max_concurrent_updates`, порядок по чату или пользователю включается явно |
| Типы Bot API | модели pydantic, пишутся и обновляются вручную | модели pydantic, **генерируются** из официальной спецификации |

## Одно и то же, в двух стилях

**Команда с аргументами.**

```python
# aiogram
@router.message(Command("sum"))
async def sum_handler(message: Message, command: CommandObject):
    if not command.args or len(command.args.split()) != 2:
        await message.answer("Использование: /sum 2 3")
        return
    a, b = map(int, command.args.split())
    await message.answer(f"{a + b}")
```

```python
# selfrotgram
class Sum(MessageHandler[BaseContext[TextMessage]]):
    cmd = Command("sum", args_count=2)          # /sum с другим числом аргументов не подходит
    query = cmd

    async def handle(self):
        a, b = (int(x) for x in self.cmd.parse(self.ctx).args)
        await self.ctx.message.answer(f"{a + b}")
```

**Команда с типизированными аргументами.**

```python
# aiogram: args это одна строка, всё остальное вручную
@router.message(Command("calc"))
async def calc(message: Message, command: CommandObject):
    try:
        one, operator, two = command.args.split()
        result = int(one) + int(two) if operator == "+" else ...
    except (AttributeError, ValueError):
        await message.answer("Использование: /calc 2 + 3")
```

```python
# selfrotgram: форма аргументов описана один раз
class CalcArgs(CommandArgs):
    one: int
    operator: Literal["+", "-", "*", "/"]
    two: int

class Calc(MessageHandler[BaseContext[TextMessage]]):
    cmd = Command("calc", CalcArgs)
    query = cmd

    async def handle(self):
        args = self.cmd.parse(self.ctx)      # args.one: int, args.operator: Literal[...]
        # неверные аргументы: CommandArgsError с .usage, его ловит on_error
```

**Кнопка с данными.**

```python
# aiogram
class Duel(CallbackData, prefix="duel"):
    duel_id: int
    action: str

@router.callback_query(Duel.filter(F.action == "accept"))
async def accept(callback: CallbackQuery, callback_data: Duel):
    await callback.answer(f"Дуэль {callback_data.duel_id}")
```

```python
# selfrotgram
class Duel(CallbackPayload, prefix="duel"):
    duel_id: int
    action: Literal["accept", "decline"]        # значение проверяется при разборе

class Accept(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    duel = Duel.filter(action="accept")
    query = duel

    async def handle(self):
        data = self.duel.parse(self.ctx)         # Duel, duel_id уже int
        await self.ctx.callback_query.answer(f"Дуэль {data.duel_id}")
```

**Многошаговый диалог.**

```python
# aiogram
class Form(StatesGroup):
    age = State()

@router.message(Form.age)
async def got_age(message: Message, state: FSMContext):
    data = await state.get_data()                # dict: ключи и типы на совести автора
    name = data.get("name")                      # может оказаться None
```

```python
# selfrotgram
class AgeStep(BaseModel):
    name: str

class Form(States):
    age = State(AgeStep)                         # состояние знает тип своих данных

class GotAge(MessageHandler[BaseContext[TextMessage]]):
    query = InState(Form.age) & HasText()

    async def handle(self):
        data = await self.ctx.fsm.get(Form.age)  # AgeStep: data.name это str
```

**Сессия БД на апдейт.**

```python
# aiogram
class DbMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with session_factory() as session:
            data["session"] = session            # хендлер получит его аргументом `session`
            return await handler(event, data)
```

```python
# selfrotgram
class DatabaseMiddleware(BaseMiddleware[AppContext]):
    async def pre_handle(self) -> bool:
        self.session = session_factory()
        self._token = session_context.set(self.session)   # ContextVar
        return True

    async def post_handle(self, exc=None):
        await (self.session.rollback() if exc else self.session.commit())
        session_context.reset(self._token)
        await self.session.close()

# в хендлере: self.ctx.db  (свойство контекста читает ContextVar)
```

## Что сделано иначе и почему

- **Класс вместо функции.** У класса есть места для `pre_handle`, `handle`, `on_error`, поля
  для промежуточных результатов (`self.age`), фильтр-атрибут, из которого потом достают
  разобранное (`self.cmd.parse(...)`). Цена: чуть больше строк на простой хендлер.
- **Нет неявной передачи аргументов.** Она удобна, пока хендлеров мало. Когда их сто, трудно
  ответить на вопрос «откуда взялся `session` в этом хендлере». Здесь ответ всегда один:
  `self.ctx`.
- **Тип и проверка вместе.** Гарантию даёт фильтр, заголовок её обещает, библиотека
  сверяет. В aiogram `message.text` остаётся `str | None` до вашей проверки.
- **Порядок выполнения простой.** Побеждает первый подошедший хендлер, сначала свои
  `handlers` роутера по порядку, потом дочерние роутеры. Запасной хендлер ставят ниже
  точного (пример: `Sum` и `SumUsage` в примерах).

## Чего здесь нет (а в aiogram есть)

- **Локализация** (`aiogram.utils.i18n`) и **сцены** (`Scenes`).
- **Хранилища FSM кроме памяти:** есть интерфейс `Storage` из трёх методов, готового
  Redis-класса пока нет.
- **Хелперы:** форматирование (`aiogram.utils.formatting`), deep-link, `ChatActionSender`,
  скачивание файлов (`bot.download`), сборщик reply-клавиатур. Есть `html.escape` из
  стандартной библиотеки и `InputFile` для загрузки.
- **Загрузка файлов внутри альбомов** (`attach://` для `send_media_group` с файлами).
- Экосистема: готовые плагины, ответы на StackOverflow, обкатка на реальных нагрузках.

## Что есть здесь, а в aiogram нет

- Проверка заголовка хендлера против фильтра при импорте, типы `TextMessage`,
  `DataCallbackQuery`, `UserMessage` и другие для каждого необязательного поля.
- FSM с типизированными данными состояния и TTL.
- `pressed_by`, `FromUser`, `MemberJoined`/`MemberLeft`, фильтры-комбинаторы для любых
  фильтров.
- `on_error` на конкретном хендлере.
- Проверка лимитов Telegram до отправки (64 байта `callback_data`, 8 кнопок в ряду).
- Типы Bot API генерируются из спецификации: после нового релиза Bot API достаточно
  перегенерировать.
