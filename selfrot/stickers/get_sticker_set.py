from typing import ClassVar
from ..methods.base import TelegramAPIMethod
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class GetStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getStickerSet"
    name: str