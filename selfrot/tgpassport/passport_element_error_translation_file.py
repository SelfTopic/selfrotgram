from pydantic import BaseModel

class PassportElementErrorTranslationFile(BaseModel):
    source: str
    type: str
    file_hash: str
    message: str