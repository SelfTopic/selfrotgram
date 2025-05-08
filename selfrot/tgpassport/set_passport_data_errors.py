from typing import Union, List, ClassVar
from ..methods import TelegramAPIMethod
from dataclasses import dataclass
from .passport_element_error import [PassportElementError

@dataclass
class SetPassportDataErrors(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setPassportDataErrors"
    user_id: int
    errors: Union[List[PassportElementError]]