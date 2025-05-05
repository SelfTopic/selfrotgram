from pydantic import BaseModel


class BackgroundFillSolid(BaseModel):
    type: str
    color: int