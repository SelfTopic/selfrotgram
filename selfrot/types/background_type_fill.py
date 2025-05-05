from pydantic import BaseModel
from .background_fill import BackgroundFill

class BackgroundTypeFill(BaseModel):
    type: str
    fill: BackgroundFill
    dark_theme_dimming: int