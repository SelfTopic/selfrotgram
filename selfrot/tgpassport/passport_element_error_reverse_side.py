from pydantic import BaseModel


class PassportElementErrorReverseSide(BaseModel):
    source: str
    type: str
    file_hash: str
    message: str