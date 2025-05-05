from typing import List
from pydantic import BaseModel


class BackgroundFillFreeformGradient(BaseModel):
    type: str
    colors: List[int]