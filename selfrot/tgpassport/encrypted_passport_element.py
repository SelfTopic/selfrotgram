from typing import Union, List, Optional
from pydantic import BaseModel
from .passport_file import [PassportFile
from .passport_file import PassportFile

class EncryptedPassportElement(BaseModel):
    type: str
    data: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    files: Optional[Union[List[PassportFile]]] = None
    front_side: Optional[Union[PassportFile]] = None
    reverse_side: Optional[Union[PassportFile]] = None
    selfie: Optional[Union[PassportFile]] = None
    translation: Optional[Union[List[PassportFile]]] = None
    hash: str