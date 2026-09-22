# Как выпускать версии

Публикация на PyPI идёт из GitHub Actions (`.github/workflows/publish.yml`) **без токена**: PyPI
заранее доверяет этому репозиторию и этому файлу (trusted publishing). Никакой секрет нигде не
хранится, поэтому его нельзя потерять или украсть.

## Один раз: настройка (в браузере)

1. **Аккаунты:** на [pypi.org](https://pypi.org/account/register/) и на
   [test.pypi.org](https://test.pypi.org/account/register/) (это два независимых сайта). Двухфакторная
   аутентификация обязательна.
2. **Доверенный издатель** (на каждом из сайтов): «Your account → Publishing → Add a new pending
   publisher», поля:

   | Поле | pypi.org | test.pypi.org |
   |---|---|---|
   | PyPI Project Name | `selfrotgram` | `selfrotgram` |
   | Owner | `SelfTopic` | `SelfTopic` |
   | Repository name | `selfrotgram` | `selfrotgram` |
   | Workflow name | `publish.yml` | `publish.yml` |
   | Environment name | `pypi` | `testpypi` |

   Имена должны совпасть буква в букву, иначе публикация отклонится.
3. **Окружения на GitHub:** репозиторий → Settings → Environments → создать `pypi` и `testpypi`.
   Для `pypi` стоит включить «Required reviewers» и добавить себя: перед настоящей публикацией
   GitHub попросит нажать «Approve» (защита от случайного тега).

## Каждый выпуск

1. Поменять `version` в `pyproject.toml` (правила: в `CHANGELOG.md`).
2. Дописать `CHANGELOG.md`.
3. Закоммитить, запушить, дождаться зелёного CI.
4. Поставить тег и запушить его: `git tag -a v0.1.2 -m "..."` и `git push origin v0.1.2`.
   Workflow соберёт пакет, сверит версию с тегом, проверит метаданные и опубликует на PyPI.
5. Проверить: `pip install selfrotgram==0.1.2` в чистом окружении.

## Репетиция на TestPyPI

Actions → Publish → Run workflow → `target: testpypi` (можно запускать с ветки `main`). Потом:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ selfrotgram
```

(`--extra-index-url` нужен, чтобы зависимости вроде `pydantic` брались с настоящего PyPI.)

## Правила безопасности, встроенные в workflow

- на настоящий PyPI публикуется только с **тега** (`github.ref_type == 'tag'`), с ветки нельзя;
- версия в `pyproject.toml` обязана совпасть с тегом, иначе сборка падает;
- право получать токен публикации (`id-token: write`) есть только у заданий публикации.

## Если что-то пошло не так

- **Версию нельзя перезаписать и нельзя загрузить заново**, даже если её удалили. Ошибка в
  опубликованной версии исправляется новой (`0.1.1`). Плохую можно пометить «yanked» на
  странице проекта: `pip` перестанет выбирать её по умолчанию.
- **«Trusted publisher not found» / «invalid-publisher»:** имена в настройке PyPI не совпали с
  репозиторием, файлом workflow или окружением; сверить таблицу выше.
- **Заброшенный проект:** публиковать больше не обязательно. Уже выпущенные версии остаются
  установимыми. Если поддержки не будет, честно напишите это в README.
