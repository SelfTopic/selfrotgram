from typing import Optional, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass

@dataclass
class GetUserProfilePhotos(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getUserProfilePhotos"
    user_id: int
    offset: Optional[int] = None
    limit: Optional[int] = None