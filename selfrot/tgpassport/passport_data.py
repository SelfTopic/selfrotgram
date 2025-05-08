from typing import Union, List
from pydantic import BaseModel
from .encrypted_passport_element import [EncryptedPassportElement
from .encrypted_credentials import EncryptedCredentials

class PassportData(BaseModel):
    data: Union[List[EncryptedPassportElement]]
    credentials: EncryptedCredentials