import importlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

from selfrot.cli import main
from selfrot.cli.init import InitError, init_project

from .conftest import FakeTelegram, bind, message_update

ROOT = Path(__file__).resolve().parent.parent

EXPECTED = {
    ".env.example",
    "src/__init__.py",
    "src/bot/__init__.py",
    "src/bot/__main__.py",
    "src/bot/bot.py",
    "src/bot/context.py",
    "src/bot/routers/__init__.py",
    "src/bot/routers/start.py",
    "src/bot/keyboards/__init__.py",
    "src/bot/middlewares/__init__.py",
    "src/bot/filters/__init__.py",
}


def tree(root: Path) -> set[str]:
    return {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()}


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Пустая папка проекта; импорты сгенерированного кода не оседают между тестами."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    before = set(sys.modules)
    yield tmp_path
    for name in set(sys.modules) - before:
        if name.split(".")[0] in {"src", "app", "mybot"}:
            del sys.modules[name]


class TestInit:
    def test_creates_the_agreed_tree_and_nothing_else(self, project):
        result = init_project(project)
        assert tree(project) == EXPECTED
        assert len(result.created) == len(EXPECTED)
        assert result.module == "src.bot"

    def test_empty_places_are_really_empty(self, project):
        init_project(project)
        for name in ("keyboards", "middlewares", "filters"):
            assert (project / "src/bot" / name / "__init__.py").read_text() == ""

    def test_dry_run_creates_nothing(self, project):
        result = init_project(project, dry_run=True)
        assert tree(project) == set()
        assert len(result.created) == len(EXPECTED)

    def test_never_overwrites_existing_files(self, project):
        init_project(project)
        edited = project / "src/bot/context.py"
        edited.write_text("# моё\n")
        (project / ".env.example").write_text("BOT_TOKEN=mine\n")

        result = init_project(project)
        assert edited.read_text() == "# моё\n"
        assert (project / ".env.example").read_text() == "BOT_TOKEN=mine\n"
        assert result.created == []
        assert len(result.skipped) == len(EXPECTED)

    def test_fills_only_the_missing_files(self, project):
        init_project(project)
        (project / "src/bot/bot.py").unlink()
        result = init_project(project)
        assert [p.name for p in result.created] == ["bot.py"]

    def test_custom_package_path(self, project):
        result = init_project(project, "app/bot")
        assert result.module == "app.bot"
        assert (project / "app/__init__.py").exists()
        assert (project / "app/bot/__main__.py").exists()
        assert not (project / "src").exists()

    def test_single_level_package(self, project):
        init_project(project, "mybot")
        assert (project / "mybot/__main__.py").exists()
        assert (project / "mybot/routers/start.py").exists()

    @pytest.mark.parametrize(
        "path", ["my-bot", "src/1bot", "class", "../out", "/abs/bot", ""]
    )
    def test_bad_package_paths(self, project, path):
        with pytest.raises(InitError):
            init_project(project, path)

        assert tree(project) == set()


class TestGeneratedProject:
    def test_imports_and_builds_a_dispatcher(self, project):
        init_project(project)
        module = importlib.import_module("src.bot.__main__")
        dispatcher = module.Dispatcher(token="123456:TEST-token")
        assert dispatcher.used_update_types() == {
            "message"
        }  # стартовый роутер подключён

    def test_custom_package_also_works(self, project):
        init_project(project, "app/bot")
        module = importlib.import_module("app.bot.__main__")
        assert module.Dispatcher(token="123456:TEST-token").used_update_types() == {
            "message"
        }

    async def test_start_command_is_answered(self, project, telegram: FakeTelegram):
        init_project(project)
        module = importlib.import_module("src.bot.__main__")
        dispatcher = module.Dispatcher(token="123456:TEST-token")

        await dispatcher._handle(
            dispatcher.create_context(bind(message_update("/start"), dispatcher.api))
        )
        await dispatcher._handle(
            dispatcher.create_context(bind(message_update("привет"), dispatcher.api))
        )
        assert [m["text"] for m in telegram.sent] == ["Привет! Я бот на selfrotgram."]
        await dispatcher.api.close_session()

    def test_without_token_stops_with_a_clear_message_and_writes_nothing(
        self, project, monkeypatch
    ):
        init_project(project)
        monkeypatch.delenv("BOT_TOKEN", raising=False)
        module = importlib.import_module("src.bot.__main__")

        with pytest.raises(SystemExit) as info:
            module.main()

        assert "BOT_TOKEN" in str(info.value)
        assert not (
            project / "bot_cfg.cfg"
        ).exists()  # не подхватывает старый файл настроек

    def test_env_example_asks_for_the_token(self, project):
        init_project(project)
        text = (project / ".env.example").read_text()
        assert "BOT_TOKEN=" in text
        assert "# WEBHOOK_URL" in text  # вебхук закомментирован: по умолчанию поллинг


class TestCommandLine:
    def test_init_command(self, project, capsys):
        assert main(["init"]) == 0
        output = capsys.readouterr().out
        assert "+ src/bot/__main__.py" in output
        assert "python -m src.bot" in output
        assert ".gitignore" in output  # напоминание про .env
        assert tree(project) == EXPECTED

    def test_second_run_reports_nothing_to_do(self, project, capsys):
        main(["init"])
        capsys.readouterr()
        assert main(["init"]) == 0
        assert "Ничего не создано" in capsys.readouterr().out

    def test_dry_run_flag(self, project, capsys):
        assert main(["init", "--dry-run"]) == 0
        assert "Было бы создано" in capsys.readouterr().out
        assert tree(project) == set()

    def test_invalid_path_is_an_error_not_a_traceback(self, project, capsys):
        assert main(["init", "my-bot"]) == 1
        assert "my-bot" in capsys.readouterr().err

    def test_python_dash_m_selfrot(self, project):
        env = {**os.environ, "PYTHONPATH": str(ROOT)}
        done = subprocess.run(
            [sys.executable, "-m", "selfrot", "init", "app/bot"],
            cwd=project,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        assert done.returncode == 0, done.stderr
        assert (project / "app/bot/__main__.py").exists()
        assert "python -m app.bot" in done.stdout

    def test_version(self, capsys):
        with pytest.raises(SystemExit) as info:
            main(["--version"])
        assert info.value.code == 0
        assert "selfrotgram" in capsys.readouterr().out
