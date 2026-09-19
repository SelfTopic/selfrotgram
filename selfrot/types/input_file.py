import asyncio
import mimetypes
import os
from pathlib import Path


class InputFile:
    """
    Файл для загрузки в Telegram. Строка (file_id или URL) передаётся как есть,
    а загружаемый файл — так:

        InputFile.from_path("cat.jpg")
        InputFile(b"...", "report.txt")
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
