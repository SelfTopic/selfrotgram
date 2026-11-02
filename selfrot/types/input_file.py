import asyncio
import mimetypes
import os
from pathlib import Path
from typing import Any, BinaryIO

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class InputFile:
    """
    Файл для загрузки в Telegram. Строка (file_id или URL) передаётся как есть,
    а загружаемый файл — так:

        InputFile.from_path("cat.jpg")
        InputFile(b"...", "report.txt")

    Годится и аргументом метода (send_photo(photo=...)), и полем объекта
    (InputMediaPhoto(media=...) в альбоме): ссылку attach://… библиотека
    подставит сама. Файл с диска уходит в сеть частями, целиком в память
    не читается.
    """

    def __init__(self, source: bytes | Path, filename: str | None = None) -> None:
        self._source = source
        self.filename = filename or (
            source.name if isinstance(source, Path) else "file"
        )

    @classmethod
    def from_path(
        cls, path: str | os.PathLike[str], filename: str | None = None
    ) -> "InputFile":
        return cls(Path(path), filename)

    @property
    def content_type(self) -> str:
        return mimetypes.guess_type(self.filename)[0] or "application/octet-stream"

    async def read(self) -> bytes:
        if isinstance(self._source, Path):
            return await asyncio.to_thread(self._source.read_bytes)

        return self._source

    async def _open(self) -> bytes | BinaryIO:
        """Что отдать в multipart: байты как есть, файл — открытым (закрывает вызывающий)."""
        if isinstance(self._source, Path):
            return await asyncio.to_thread(self._source.open, "rb")

        return self._source

    def __repr__(self) -> str:
        return f"InputFile({self.filename!r})"

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        # Поле объекта (InputMediaPhoto.media: InputFile | str) хранит сам объект:
        # в JSON он не превращается, вместо него сериализация метода ставит attach://….
        return core_schema.is_instance_schema(cls)
