from typing import Union, Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from ..types import ChatAdministratorRights

@dataclass
class SetMyDefaultAdministratorRights(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setMyDefaultAdministratorRights"
    rights: Optional[Union[ChatAdministratorRights]] = None
    for_channels: Optional[bool] = None