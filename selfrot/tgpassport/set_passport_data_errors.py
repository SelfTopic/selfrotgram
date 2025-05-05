from typing import ClassVar
from methods.base import TelegramAPIMethod
from dataclasses import dataclass


@dataclass
class SetPassportDataErrors(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setPassportDataErrors"
    user_id: int
    errors: List[PassportElementError]