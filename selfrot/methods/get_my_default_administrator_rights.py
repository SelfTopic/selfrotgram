from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetMyDefaultAdministratorRights(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getMyDefaultAdministratorRights"
    for_channels: Optional[bool] = None