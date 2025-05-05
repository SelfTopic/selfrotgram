from pydantic import BaseModel


class PassportElementErrorSelfie(BaseModel):
    source: str
    type: str
    file_hash: str
    message: str