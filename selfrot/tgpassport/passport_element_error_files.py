from typing import List
from pydantic import BaseModel


class PassportElementErrorFiles(BaseModel):
    source: str
    type: str
    file_hashes: List[str]
    message: str