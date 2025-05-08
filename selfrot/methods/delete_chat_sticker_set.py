from typing import Union, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class DeleteChatStickerSet(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "deleteChatStickerSet"
    chat_id: Union[int, str]