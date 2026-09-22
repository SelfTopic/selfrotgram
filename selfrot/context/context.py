import asyncio
import inspect
import os
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar

from ..client import Bot
from ..deferred import BackgroundTasks, Deferred
from ..exceptions import ContextError, DefinitionError, FileNotAvailableError
from ..fsm import FSM
from ..types import Update
from .accessors import TEvent
from .methods import ContextMethods

if TYPE_CHECKING:
    from ..handlers.base import BaseHandler

TContext = TypeVar("TContext", bound="BaseContext[Any]")


def _write_new(path: Path, data: bytes) -> Path:
    """
    Пишет, не трогая чужой файл: если path занят, пробует " (1)", " (2)", ... до первого
    свободного имени. Каждая попытка через open(..., "xb") — атомарное «создать, если нет»
    на уровне ОС, а не «проверили exists(), потом записали» (между проверкой и записью
    файл мог появиться, например от другого апдейта в соседней задаче).
    """
    stem, suffix = path.stem, path.suffix
    candidate, n = path, 1
    while True:
        try:
            with open(candidate, "xb") as f:
                f.write(data)
            return candidate
        except FileExistsError:
            candidate = path.with_name(f"{stem} ({n}){suffix}")
            n += 1


@dataclass
class BaseContext(ContextMethods[TEvent]):
    update: Update
    bot: Bot
    # Прикрепляет диспетчер. Не аргумент конструктора: пользовательские контексты
    # собираются как self.context(update, api, сервисы...) и ничего не замечают.
    _fsm: FSM | None = field(default=None, init=False, repr=False, compare=False)

    # Отложенные вызовы этого апдейта и реестр диспетчера (прикрепляет диспетчер).
    _deferred: list[Deferred] = field(
        default_factory=list, init=False, repr=False, compare=False
    )
    _background: BackgroundTasks | None = field(
        default=None, init=False, repr=False, compare=False
    )

    def defer(
        self,
        fn: Callable[..., Awaitable[Any]],
        *args: Any,
        delay: float = 0.0,
        owner: "BaseHandler[Any] | None" = None,
        **kwargs: Any,
    ) -> Deferred:
        """
        Вызвать async-функцию позже, после закрытия хендлера и мидлварей, через delay
        секунд. Для хендлера удобнее self.defer(...): ошибка тогда пойдёт в его on_error.
        """
        if self._background is None:
            raise ContextError(
                "У контекста нет реестра отложенных вызовов: он создан не диспетчером"
            )
        if not inspect.iscoroutinefunction(fn):
            raise DefinitionError(
                f"defer() принимает async-функцию (у неё await), получено {fn!r}"
            )
        if delay < 0:
            raise DefinitionError(
                f"defer(): delay не может быть отрицательным ({delay})"
            )

        deferred = Deferred(fn, args, kwargs, delay, ctx=self, owner=owner)
        self._background.register(deferred)  # DeferredLimitError, если места нет
        self._deferred.append(deferred)
        return deferred

    async def download(
        self, destination: str | os.PathLike[str], *, overwrite: bool = True
    ) -> Path:
        """
        Файл текущего апдейта (фото — самый большой размер, иначе animation/audio/
        document/sticker/video/video_note/voice — что заполнено; ничего нет у самого
        сообщения — берёт из reply_to_message) в destination. У destination нет
        расширения ("photo", а не "photo.jpg") — оно берётся из оригинального имени файла
        (animation/audio/document/video, как называл его отправитель), а если его нет —
        из настоящего file_path, который вернул Telegram (".jpg", ".oga", ...). Не
        угадывается по виду медиа. Указали своё расширение — оно и остаётся.

        overwrite=True (по умолчанию) — существующий файл на destination молча
        перезаписывается. overwrite=False — существующий файл не трогается, а к имени
        добавляется " (1)", " (2)", ... до первого свободного (как в проводнике).
        Возвращённый Path тогда может отличаться от destination.

        Ничего скачиваемого нет — ContextError.

        Файл не из этого апдейта, а по известному file_id? self.bot.download(file_id)
        (или self.bot.download_file(file_path), если file_path уже под рукой) — байты,
        без записи на диск.
        """
        file_id, original_name = self._downloadable_file_id()
        file = await self.bot.get_file(file_id)
        if file.file_path is None:
            raise FileNotAvailableError(
                f"getFile({file_id!r}) не вернул file_path: файл недоступен для скачивания"
            )

        data = await self.bot.download_file(file.file_path)
        path = Path(destination)
        if not path.suffix:
            suffix = Path(original_name).suffix if original_name else ""
            path = path.with_suffix(suffix or Path(file.file_path).suffix)

        if overwrite:
            await asyncio.to_thread(path.write_bytes, data)
            return path

        return await asyncio.to_thread(_write_new, path, data)

    @property
    def fsm(self) -> FSM:
        """Состояние диалога этого пользователя в этом чате."""
        if self._fsm is None:
            raise ContextError(
                "У контекста нет FSM: он создан не диспетчером "
                "(в тесте прикрепите FSM(storage, key) к ctx._fsm)"
            )

        return self._fsm
