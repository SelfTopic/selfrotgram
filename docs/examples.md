# Путеводитель по примерам

Здесь каждый пример из папки [`examples/`](../examples) разобран по кусочкам, простыми
словами. Идти лучше по порядку: каждый следующий пример добавляет одну новую мысль.

## Сначала одна картинка в голове

Представьте почтовое отделение. Телеграм приносит письма (сообщения пользователей), а ваш бот
их разбирает.

| В библиотеке | В отделении |
|---|---|
| **Dispatcher** (диспетчер) | сортировщик: берёт письмо и решает, кому его отдать |
| **Handler** (хендлер) | сотрудник, который отвечает на один вид писем |
| **Filter** (фильтр, поле `query`) | охранник у двери сотрудника: «пропускаю только письма с текстом» |
| **Context** (`self.ctx`) | папка с письмом и всем, что нужно сотруднику: письмо, отправитель, телефон для ответа |
| **Router** (роутер) | отдел: группа сотрудников. Отделы можно вкладывать друг в друга |
| **Middleware** (мидлварь) | проходная на входе: что-то делает до сотрудника и после него |
| **FSM** (состояние) | анкета на много шагов: бот помнит, на каком ты вопросе |

Правило сортировщика простое: он идёт по сотрудникам по порядку, и **письмо достаётся
первому, чей охранник его пропустил**. Остальные письма не видят.

## Как запустить любой пример

```bash
python -m examples.echo_bot
```

Токен берётся из переменной `BOT_TOKEN` или, если её нет, из файла `bot_cfg.cfg` в текущей
папке (`bot_token = 123456:ABC`). Остановка: `Ctrl+C`. Пока бот ждёт сообщений, он ничего
не пишет, это нормально; при старте будет строка «Запущен @имя_бота».

Один токен нельзя запускать в двух местах сразу: Telegram отдаёт письма кому-то одному, и
вы получите ошибку 409.

---

## 1. `echo_bot`: бот, который повторяет

**Что делает:** отвечает на любой текст тем же текстом с приставкой «Echo:».
**Попробуйте:** напишите боту «привет».

```python
class EchoHandler(MessageHandler[BaseContext[TextMessage]]):
    query = HasText()

    async def handle(self) -> None:
        await self.ctx.answer_message(f"Echo: {self.ctx.message.text}")
```

Разбор:

- `EchoHandler` это сотрудник. `MessageHandler` значит «я работаю с обычными сообщениями».
- `query = HasText()` это охранник: «пропускаю, только если в сообщении есть текст». Фото без
  подписи он не пропустит.
- `TextMessage` в заголовке это обещание: «с текстом, а не с пустотой». Из-за него
  `self.ctx.message.text` это точно строка, и не нужно проверять `if text is None`. Обещание
  и охранник обязаны совпадать, иначе библиотека ругнётся при запуске.
- `handle()` это работа сотрудника. `answer_message` отправляет ответ в тот же чат.

Дальше в файле собирается отдел:

```python
class Dispatcher(BaseDispatcher[BaseContext[TextMessage]]):
    bot = Bot
    context = BaseContext
    handlers = (EchoHandler,)
    middlewares = (LoggingMiddleware,)
```

`handlers` это список сотрудников по порядку. `LoggingMiddleware` это проходная, которая
записывает в лог, сколько времени заняло письмо.

**Запомните:** хендлер + фильтр + обещание типа. Больше ничего для простого бота не нужно.

## 2. `filtered_bot`: свой охранник

**Что делает:** в личке повторяет текст, в группе отвечает, что тут он не эхо-бот.
**Попробуйте:** напишите боту в личку, потом добавьте в группу и напишите там.

Своего охранника пишут одной функцией `check`:

```python
class IsPrivate(BaseFilter[BaseContext[Any]]):
    async def check(self, ctx: BaseContext[Any]) -> bool:
        chat = ctx.chat
        return chat is not None and chat.type == "private"
```

И складывают с готовым знаком `&` («и»):

```python
class PrivateEcho(MessageHandler[BaseContext[TextMessage]]):
    query = HasText() & IsPrivate()

class GroupNote(MessageHandler[BaseContext[TextMessage]]):
    query = HasText() & ~IsPrivate()      # ~ значит «не»
```

Охранники складываются: `&` («оба»), `|` («любой из»), `~` («не»). Проверка идёт слева
направо и останавливается, как только ответ известен. Поэтому дорогую проверку (в базу)
ставят справа.

**Запомните:** свой фильтр это класс с одним методом `check`.

## 3. `deps_bot`: свои инструменты в папке

**Что делает:** здоровается по имени.
**Попробуйте:** напишите что угодно.

Иногда хендлеру нужен инструмент, не имеющий отношения к Телеграму: сервис приветствий, доступ
к базе, настройки. Их кладут в **контекст**, в папку сотрудника:

```python
@dataclass
class DepsContext(BaseContext):
    greeter: GreetingService
```

Диспетчер создаёт такую папку на каждое письмо, поэтому ему говорят, как:

```python
def create_context(self, update: Update) -> DepsContext:
    return self.context(update, self.api, self.greeter)
```

А хендлер берёт инструмент из папки:

```python
await self.ctx.answer_message(self.ctx.greeter.greet(name))
```

Никакой магии: откуда взялся `greeter`, видно прямо в коде. Инструмент, который живёт всё
время работы бота, создают один раз (в `__init__` диспетчера).

**Запомните:** свои зависимости это поля вашего подкласса `BaseContext`.

## 4. `errors_bot`: когда что-то пошло не так

**Что делает:** показывает три сорта ошибок.
**Попробуйте:** `/rename ab`, `/rename Вася`, `/buy`, `/bug`.

Придумаем ошибку «это можно показать пользователю»:

```python
class UserError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
```

Любое место кода может её «бросить»: `raise UserError("Имя короче 3 символов")`. Поймать её можно
на двух уровнях.

**На конкретном хендлере**, если он знает, как ответить особым образом:

```python
class Buy(MessageHandler[BaseContext[TextMessage]]):
    async def handle(self):
        raise NotEnoughMoney(price=100, balance=30)

    async def on_error(self, exc: Exception) -> None:
        if isinstance(exc, NotEnoughMoney):
            await self.ctx.reply_message(f"Не хватает денег: {exc.message}")
            return
        raise exc                       # не моя ошибка: пусть разбирается диспетчер
```

**На диспетчере**, одно правило на весь бот:

```python
async def on_error(self, ctx: BaseContext, exc: Exception) -> None:
    if isinstance(exc, UserError):
        await ctx.reply_message(exc.message)     # свою ошибку показываем
        return
    await super().on_error(ctx, exc)             # чужую только пишем в лог
```

Обычный сбой (`/bug`) пользователь не видит: показывать ему текст вроде «relation users does
not exist» нельзя. Он попадает только в лог.

Ещё одна мысль в этом примере: проверку удобно делать в `pre_handle`. Это шаг «до основной
работы». Если он упал, `handle` уже не запускается, а ошибка идёт в `on_error`.

**Запомните:** `raise exc` в `on_error` значит «это не моё, передаю выше».

## 5. `keyboards_bot`: кнопки

**Что делает:** викторина с кнопками и дуэль, где нажать может только свой.
**Попробуйте:** `/quiz`, потом `/duel` и нажмите кнопку. Затем нажмите её с другого аккаунта.

Кнопки собирает `InlineKeyboard`:

```python
keyboard = InlineKeyboard(width=2)            # по 2 кнопки в ряд
for index, option in enumerate(OPTIONS):
    keyboard.button(option, QuizAnswer(question_id=1, option=index))
await self.ctx.message.reply("Кто такой Канеки?", reply_markup=keyboard.markup())
```

Когда пользователь нажимает кнопку, Telegram присылает строку. Раньше её собирали руками
(`"duel:12:accept:5"`) и так же руками разбирали. Здесь для этого есть **типизированные
данные кнопки**:

```python
class Duel(CallbackPayload, prefix="duel"):
    duel_id: int
    action: Literal["consent_initiator", "consent_target", "fora_serious"]
    expected_id: int          # кто имеет право нажать
```

Библиотека сама упаковывает их в строку и достаёт обратно уже с правильными типами. Если
строка слишком длинная для Telegram (лимит 64 байта) или не тот формат, вы узнаете об этом
сразу.

Обработчик нажатия:

```python
class Consent(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    duel = Duel.filter(action="consent_target").pressed_by("expected_id")
    query = duel

    async def handle(self):
        data = self.duel.parse(self.ctx)     # data.duel_id — число
        await self.ctx.edit_message_text(f"Дуэль {data.duel_id} принята")
```

`.pressed_by("expected_id")` значит «пропускай, только если нажал человек, чей номер лежит в
этом поле». Кнопку в группе видят все, а нажать по-настоящему может один.

Кто нажал не тот, письмо идёт дальше по списку, к следующему сотруднику:

```python
class NotForYou(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    query = Duel.filter(action="consent_target")       # та же кнопка, но без проверки
    async def handle(self):
        await self.ctx.callback_query.answer("Эта кнопка не для тебя", show_alert=True)
```

Он стоит **после** `Consent` в списке `handlers`. Порядок важен: сначала строгий, потом
запасной.

**Запомните:** данные кнопки это класс с полями; хендлеры-соседи по порядку ловят своих и
чужих.

## 6. `fsm_bot`: анкета на много шагов

**Что делает:** спрашивает имя, потом возраст, потом просит подтвердить.
**Попробуйте:** `/form`, ответьте на вопросы. Попробуйте написать вместо возраста слово,
нажать `/cancel` посередине, и сначала «нет» вместо «да».

Сначала описываем **шаги** и то, что бот запоминает на каждом:

```python
class AgeStep(BaseModel):
    name: str                      # на шаге «возраст» бот уже знает имя

class ConfirmStep(AgeStep):
    age: int                       # на шаге «подтверждение» знает и возраст

class Form(States):
    name = State()                 # ничего не помним
    age = State(AgeStep)           # помним AgeStep
    confirm = State(ConfirmStep)
```

Шаг знает, **какого вида данные** к нему привязаны. Поэтому нельзя случайно положить не то:
редактор подсветит ошибку.

Хендлер шага ловит письма, только пока человек на этом шаге:

```python
class GotAge(MessageHandler[BaseContext[TextMessage]]):
    query = InState(Form.age) & HasText()

    async def pre_handle(self):
        self.age = int(self.ctx.message.text)         # ValueError уйдёт в on_error

    async def handle(self):
        previous = await self.ctx.fsm.get(Form.age)   # AgeStep, previous.name — строка
        await self.ctx.fsm.set(Form.confirm, ConfirmStep(name=previous.name, age=self.age))
        await self.ctx.message.answer(f"{previous.name}, {self.age}. Всё верно? (да / нет)")
```

`ctx.fsm` это «блокнот бота про этого человека в этом чате». `set` записывает, на каком шаге
он и что о нём известно, `get` читает, `clear` вырывает страницу. У каждого пользователя свой
блокнот, они не путаются.

Почему `& HasText()` рядом с `InState`? `InState` знает только шаг, но не гарантирует, что
пришёл текст, а заголовок обещает текст. Библиотека требует это дописать, чтобы обещание не
разошлось с проверкой.

Ещё две мелочи:

- `Command("cancel") & ~NoState()` значит «/cancel работает, только если анкета начата». Он
  стоит в списке выше шагов, поэтому перехватывает слово «/cancel» на любом шаге.
- `fsm_storage = MemoryStorage(ttl=600)`: брошенная анкета исчезает сама через 10 минут.
  Блокнот хранится в памяти, после перезапуска бота он пуст.

**Запомните:** шаг = состояние + тип данных; хендлер ловит человека на шаге через `InState`.

## 7. `chat_members`: кто вошёл и вышел

**Что делает:** приветствует вошедших в группу и прощается с вышедшими.
**Попробуйте:** добавьте бота в группу **администратором**, потом пригласите второй аккаунт и
заставьте его выйти.

Telegram присылает событие «статус участника изменился» с двумя значениями: «был» и «стал».
Слов «вошёл» и «вышел» в нём нет, их получают сравнением. За это отвечают готовые фильтры:

```python
class NewMember(ChatMemberHandler[BaseContext[ChatMemberUpdated]]):
    query = MemberJoined()             # раньше не был в чате, теперь в чате

class MemberGone(ChatMemberHandler[BaseContext[ChatMemberUpdated]]):
    query = MemberLeft()               # раньше был, теперь нет (вышел, удалён, заблокирован)
```

Есть два вида события. `ChatMemberHandler` про **других** участников, а `MyChatMemberHandler`
про **самого бота** («меня добавили в чат»). У них одинаковые фильтры.

**Запомните:** «вошёл» и «вышел» это сравнение «был» и «стал», а готовый фильтр делает его за вас.

## 8. `db_bot`: запоминать в базе

**Что делает:** считает, сколько сообщений написал каждый. Нужны пакеты `sqlalchemy` и
`aiosqlite`.
**Попробуйте:** пишите боту, счётчик растёт. Перезапустите бота, счёт сохранился.

Идея: на каждое письмо открываем **одну сессию базы**. Если письмо обработалось, сохраняем
(`commit`), если случилась ошибка, откатываем (`rollback`). Это работа проходной, мидлвари:

```python
class DatabaseMiddleware(BaseMiddleware[AppContext]):
    async def pre_handle(self) -> bool:            # до сотрудника
        self.session = session_factory()
        self._token = session_context.set(self.session)
        return True

    async def post_handle(self, exc=None):         # после сотрудника
        await (self.session.rollback() if exc else self.session.commit())
        session_context.reset(self._token)
        await self.session.close()
```

`exc` это ошибка сотрудника, если она была. Сессия лежит в `ContextVar`: это «ячейка на одно
письмо». Хендлер достаёт её из папки одной строкой:

```python
class AppContext(BaseContext[TEvent]):
    @property
    def db(self) -> AsyncSession:
        return session_context.get()
```

Хендлеру нужно знать отправителя, поэтому он обещает `UserMessage` и просит фильтр `HasUser()`:
`self.ctx.message.user` это `User`, а не «может быть пусто».

**Запомните:** «открыть до, закрыть после» пишется в мидлвари; хендлер только пользуется.

## 9. `webhook_bot`: получать письма не опросом, а доставкой

Есть два способа получать сообщения:

- **Поллинг:** бот сам постоянно спрашивает Телеграм: «есть новые?» Просто, работает с
  ноутбука. Так запускались все предыдущие примеры.
- **Вебхук:** Телеграм сам приходит с письмами на ваш адрес. Нужен публичный HTTPS-адрес
  (обычно nginx перед ботом). Так работают боты на сервере.

Выбор делается одной строкой при запуске:

```python
if url := os.environ.get("WEBHOOK_URL"):
    dp.start_webhook(url=url, secret_token=os.environ["WEBHOOK_SECRET"],
                     host="0.0.0.0", port=8999)
else:
    dp.start_polling()
```

`secret_token` это пароль: Телеграм подписывает им каждую доставку, а бот отвергает письма без
пароля. Без него любой мог бы прислать «письмо от администратора».

Ещё два места из этого примера:

- `on_startup` и `on_shutdown` это «открыть перед работой» и «закрыть после»: сюда кладут
  фоновые задачи, соединения. Остановка (`Ctrl+C` или `docker stop`) сначала дожидается
  начатых хендлеров.
- `class MyBot(Bot): defaults = BotDefaults(link_preview_options=...)`: настройки «для всех
  сообщений сразу», например отключить предпросмотр ссылок.

Локально вебхук не проверить: нужен адрес, доступный из интернета.

## 10. `bot_command`: как выглядит настоящий проект

Один файл на всё хорош для примера. Настоящий бот разложен по папкам:

```
bot_command/
  __main__.py       запуск
  dispatcher.py     диспетчер: собирает отделы, кладёт сервисы в контекст
  context.py        папка сотрудника (AppContext)
  routers.py        отдел BotRouter
  handlers.py       сотрудник BotHandler
  middlewares.py    проходные (запись пользователя в базу)
  services.py, repositories.py, models.py, database.py   всё остальное
```

Ключевое место:

```python
class AppDispatcher(BaseDispatcher[AppContext]):
    auto_connect = (".routers",)          # найти отделы в модуле сам
    middlewares = (SyncUserMiddleware,)
```

`auto_connect` ищет в указанном модуле переменную `router` и подключает её. Роутер (отдел)
собирается так:

```python
class BotRouter(BaseRouter[AppContext]):
    handlers = (BotHandler,)

router = BotRouter
```

**Запомните:** проект растёт деревом из отделов; у каждого свои сотрудники и проходные.

## 11. `chestor_routers`: дерево побольше

Копия структуры настоящего бота: 47 отделов, вложенных друг в друга, без хендлеров. Нужна,
чтобы посмотреть на дерево целиком:

```bash
python -m examples.chestor_routers
```

Он печатает отделы с отступами и названиями мидлварей на них. Так видно правило про
проходные: мидлварь диспетчера срабатывает на каждое письмо, а мидлварь отдела только тогда,
когда письмо идёт к сотруднику из этого отдела.

---

## Что читать дальше

- [Как устроена библиотека](design.md): те же идеи в виде схемы.
- [Отличия от aiogram](from-aiogram.md): если вы уже писали на нём.
- [Журнал решений](decisions.md): подробности и причины (для любопытных).
