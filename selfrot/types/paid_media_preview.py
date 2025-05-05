from typing import Optional
from pydantic import BaseModel


class PaidMediaPreview(BaseModel):
    type: str
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None