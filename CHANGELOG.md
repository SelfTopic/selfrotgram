# История изменений

Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), версии: [SemVer](https://semver.org/lang/ru/).
Пока версия `0.x`, минорная версия играет роль мажорной: **ломающие изменения увеличивают
минор** (`0.1` → `0.2`), исправления и совместимые добавления увеличивают патч (`0.1.0` →
`0.1.1`). Поэтому `poetry add` записывает `^0.1.0`, то есть `>=0.1.0,<0.2.0`.

## [Не выпущено]

### Добавлено
- условия над ответом на сообщение: `Reply[T]` и 13 готовых пар (`user`, `text`, `entities`,
  `caption`, `caption_entities`, `photo`, `animation`, `audio`, `document`, `sticker`, `video`,
  `video_note`, `voice`): типы `ReplyUserMessage`, `ReplyPhotoMessage`, ... и фильтры
  `HasReplyUser`, `HasReplyPhoto`, ... (генерируются; список в `REPLY_ATTRS` в
  `scripts/generate_types.py`). Несколько условий: `Reply[PhotoCaption]`, где
  `PhotoCaption` собран наследованием, и фильтр `HasReplyPhoto() & HasReplyCaption()`
- пример `examples/reply_bot.py`: бот на 9 команд, которые работают в ответ на сообщения (готовые
  условия, несколько условий сразу, «любое из», `if`, подсказка после всех команд)

### Изменено
- проверка заголовка хендлера сверяет и вложенные поля: гарантия фильтра теперь может содержать
  пути вроде `reply_to_message.user`. Раньше заголовок с вложенным суженным типом проходил проверку,
  даже если фильтр проверял только внешнее поле; теперь это `DefinitionError` при импорте

## [0.1.1] — 2026-09-20

Первая версия на PyPI (`pip install selfrotgram`). Возможности те же, что в 0.1.0; версия `0.1.0`
существует только как тег в git и на PyPI не публиковалась.

### Изменено
- упаковка для PyPI: ссылки в README абсолютные (на PyPI относительные не работают), в метаданных
  ссылки `Documentation`, `Changelog`, `Issues`
- README: установка с PyPI (`pip install selfrotgram`, `poetry add selfrotgram`), установка из git
  осталась как запасной путь

### Добавлено
- публикация на PyPI из GitHub Actions без токена (`publish.yml`, trusted publishing) и
  инструкция по выпуску версий (`docs/releasing.md`)
- проверка метаданных пакета (`twine check --strict`) в обычном CI

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

[0.1.1]: https://github.com/SelfTopic/selfrotgram/releases/tag/v0.1.1
[0.1.0]: https://github.com/SelfTopic/selfrotgram/releases/tag/v0.1.0
