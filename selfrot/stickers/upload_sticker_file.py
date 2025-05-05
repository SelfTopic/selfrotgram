from typing import ClassVar
from ..methods.base import TelegramAPIMethod
from pydantic import BaseModel
from dataclasses import dataclass
from ..types.input_file import InputFile

@dataclass
class UploadStickerFile(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "uploadStickerFile"
    user_id: int
    sticker: InputFile
    sticker_format: str