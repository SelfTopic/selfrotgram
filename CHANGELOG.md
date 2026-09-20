# История изменений

Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), версии: [SemVer](https://semver.org/lang/ru/).
Пока версия `0.x`, минорная версия играет роль мажорной: **ломающие изменения увеличивают
минор** (`0.1` → `0.2`), исправления и совместимые добавления увеличивают патч (`0.1.0` →
`0.1.1`). Поэтому `poetry add` записывает `^0.1.0`, то есть `>=0.1.0,<0.2.0`.

## [0.1.0] — 2026-09-20

Первый выпуск. Поддерживает Bot API 10.3, Python 3.11, 3.12 и 3.13.

### Добавлено

**Типы и методы (генерируются из спецификации Bot API)**
- 400 типов, 185 методов, `scripts/generate_types.py`; суженные типы (`TextMessage`,
  `DataCallbackQuery`, `UserMessage`, ...) для каждого необязательного поля
- 26 видов хендлеров по полям `Update`, фильтры `Has*`, ярлыки контекста (`ctx.answer_photo`, ...)
- методы на самих объектах: `message.answer()`, `message.edit_text()`, `callback.answer()`
- `Bot.defaults` (`parse_mode`, `link_preview_options`, ...), прокси, таймауты, повтор при 429,
  иерархия исключений от `SelfrotError`

**Хендлеры, фильтры, роутеры**
- хендлеры-классы; при создании класса заголовок (`AppContext[TextMessage]`) сверяется с
  гарантией фильтра (`DefinitionError`)
- фильтры: `Text*`, `Command`, `CallbackData*`, `CallbackPayload` (типизированные данные кнопок,
  `pressed_by`), `MemberJoined`, `MemberLeft`, `ChatMemberTransition`, `FromUser`, `InState`,
  `NoState`; комбинаторы `&`, `|`, `~`
- аргументы команд как данные: `CommandArgs`, `Rest`, необязательные аргументы,
  `CommandArgsError` с готовой подсказкой (`usage`)
- дерево роутеров (`routers`, `auto_connect`), мидлвари с `pre_handle` и `post_handle(exc)`,
  `on_error` на хендлере и на диспетчере

**Диспетчер**
- long polling и вебхуки (секрет в заголовке, дедупликация, 503 при перегрузке)
- параллельная обработка апдейтов, порядок по чату или пользователю включается явно
- `on_startup`, `on_shutdown`, остановка по `SIGINT` и `SIGTERM`
- отложенные вызовы: `self.defer(fn, delay=...)` и `after_handle()` (после закрытия хендлера)

**Диалоги и клавиатуры**
- FSM: `States`, `State(Model)` с типизированными данными, `ctx.fsm`, `MemoryStorage(ttl=...)`
- `InlineKeyboard` с проверкой лимитов Telegram

**Инструменты**
- команда `selfrot`: `init` (заготовка проекта), `add router` (файл или папка через `--module`),
  `tree` (роутеры, хендлеры и фильтры), `check` (ошибки и забытые подключения)
- 356 тестов, CI на GitHub Actions (Python 3.11–3.13, pyright, актуальность сгенерированного кода,
  установка пакета), лицензия MIT

### Известные ограничения
- нет локализации и сцен, готового хранилища FSM в Redis, скачивания файлов и загрузки файлов
  внутри альбомов, сборщика reply-клавиатур
- отложенные вызовы и `MemoryStorage` живут в памяти и пропадают при перезапуске бота
- API может меняться (альфа)

[0.1.0]: https://github.com/SelfTopic/selfrotgram/releases/tag/v0.1.0
