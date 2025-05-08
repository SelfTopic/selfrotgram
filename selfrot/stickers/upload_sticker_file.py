from typing import ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import InputFile

@dataclass
class UploadStickerFile(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "uploadStickerFile"
    user_id: int
    sticker: InputFile
    sticker_format: str