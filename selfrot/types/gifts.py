from typing import List
from pydantic import BaseModel
from .gift import Gift

class Gifts(BaseModel):
    gifts: List[Gift]