# Примеры

Каждый пример разобран по шагам и простыми словами в [путеводителе](../docs/examples.md).

Каждый файл запускается отдельно из корня репозитория. Токен берётся из переменной
`BOT_TOKEN`, а если её нет, то из `bot_cfg.cfg` в текущей папке (`bot_token = 123456:ABC`):

```bash
python -m examples.echo_bot                       # токен из bot_cfg.cfg
BOT_TOKEN=123456:ABC python -m examples.echo_bot  # или из переменной
```

Один токен — один запущенный процесс: два `getUpdates` на одном токене мешают друг другу
(ошибка 409). Остановка: `Ctrl+C`, хендлеры доработают штатно.

| Пример | Что показывает |
|---|---|
| [echo_bot.py](echo_bot.py) | минимум: один хендлер и `HasText` |
| [filtered_bot.py](filtered_bot.py) | свой фильтр, кастомный контекст |
| [errors_bot.py](errors_bot.py) | `on_error` на хендлере и диспетчере, свои исключения как ответы пользователю |
| [deferred_bot.py](deferred_bot.py) | отложенные действия: `defer` (таймеры), `after_handle` (долгая часть после закрытия хендлера) |
| [data_parsed_bot.py](data_parsed_bot.py) | аргументы команды как данные: `CommandArgs`, `Rest`, необязательные аргументы, `CommandArgsError` |
| [keyboards_bot.py](keyboards_bot.py) | `InlineKeyboard`, `CallbackPayload`, `.filter()`, `pressed_by` |
| [chat_members.py](chat_members.py) | `MemberJoined`, `MemberLeft` (`chat_member` и `my_chat_member`) |
| [fsm_bot.py](fsm_bot.py) | многошаговый диалог: `States`, типизированные данные, `InState`, TTL |
| [webhook_bot.py](webhook_bot.py) | вебхук и поллинг из одного кода, `on_startup`/`on_shutdown`, `Bot.defaults` |
| [deps_bot.py](deps_bot.py) | сервисы приложения в контексте |
| [db_bot.py](db_bot.py) | сессия БД на апдейт через мидлварь (нужны `sqlalchemy`, `aiosqlite`) |
| [bot_command/](bot_command) | модульный проект: роутеры, мидлвари, репозитории |
| [chestor_routers/](chestor_routers) | дерево из 47 роутеров (`python -m examples.chestor_routers` печатает его) |

Примеры проверяются тестами: `tests/test_examples.py` импортирует каждый и собирает
диспетчер, так что сломанный пример виден сразу.
