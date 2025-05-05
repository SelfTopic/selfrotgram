from typing import ClassVar
from ..methods.base import TelegramAPIMethod
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class DeleteStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteStickerSet"
    name: str