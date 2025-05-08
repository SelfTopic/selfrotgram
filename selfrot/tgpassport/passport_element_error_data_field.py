from pydantic import BaseModel, Field

class PassportElementErrorDataField(BaseModel):
    source: str
    type: str
    field_name: str
    data_hash: str
    message: str