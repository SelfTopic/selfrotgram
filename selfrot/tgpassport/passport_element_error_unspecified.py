from pydantic import BaseModel

class PassportElementErrorUnspecified(BaseModel):
    source: str
    type: str
    element_hash: str
    message: str