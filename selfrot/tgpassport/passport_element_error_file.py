from pydantic import BaseModel


class PassportElementErrorFile(BaseModel):
    source: str
    type: str
    file_hash: str
    message: str