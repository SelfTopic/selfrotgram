from typing import List
from pydantic import BaseModel


class Gifts(BaseModel):
    gifts: List[Gift]