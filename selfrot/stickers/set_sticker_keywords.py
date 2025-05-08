from typing import List, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetStickerKeywords(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setStickerKeywords"
    sticker: str
    keywords: Optional[List[str]] = None