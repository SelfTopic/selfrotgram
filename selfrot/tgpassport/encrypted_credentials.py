from pydantic import BaseModel

class EncryptedCredentials(BaseModel):
    data: str
    hash: str
    secret: str