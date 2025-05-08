from pydantic import BaseModel

class PassportFile(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int