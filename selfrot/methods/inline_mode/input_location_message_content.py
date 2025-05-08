from typing import Optional
from pydantic import BaseModel

class InputLocationMessageContent(BaseModel):
    latitude: float
    longitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None