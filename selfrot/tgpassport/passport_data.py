from typing import Union, List
from pydantic import BaseModel
from .encrypted_credentials import EncryptedCredentials
from .encrypted_passport_element import [EncryptedPassportElement

class PassportData(BaseModel):
    data: Union[List[EncryptedPassportElement]]
    credentials: EncryptedCredentials