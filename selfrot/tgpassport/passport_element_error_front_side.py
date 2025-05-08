from pydantic import BaseModel

class PassportElementErrorFrontSide(BaseModel):
    source: str
    type: str
    file_hash: str
    message: str