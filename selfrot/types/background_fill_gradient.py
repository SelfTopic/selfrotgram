from pydantic import BaseModel


class BackgroundFillGradient(BaseModel):
    type: str
    top_color: int
    bottom_color: int
    rotation_angle: int