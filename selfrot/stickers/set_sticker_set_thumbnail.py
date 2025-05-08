from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import InputFile

@dataclass
class SetStickerSetThumbnail(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerSetThumbnail"
    name: str
    user_id: int
    thumbnail: Optional[Union[InputFile, str]] = None
    format: str