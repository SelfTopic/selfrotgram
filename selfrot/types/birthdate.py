from typing import Optional
from pydantic import BaseModel

class Birthdate(BaseModel):
    day: int
    month: int
    year: Optional[int] = None