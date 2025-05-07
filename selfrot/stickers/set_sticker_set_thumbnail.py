from typing import Union, Optional, ClassVar
from ..methods.base import TelegramAPIMethod
from pydantic import BaseModel
from dataclasses import dataclass
from ..types.input_file import InputFile

@dataclass
class SetStickerSetThumbnail(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerSetThumbnail"
    name: str
    user_id: int
    format: str
    thumbnail: Optional[Union[InputFile, str]] = None