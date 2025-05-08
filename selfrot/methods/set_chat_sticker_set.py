from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class SetChatStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setChatStickerSet"
    chat_id: Union[int, str]
    sticker_set_name: str