from typing import List
from pydantic import BaseModel
from .business_opening_hours_interval import BusinessOpeningHoursInterval

class BusinessOpeningHours(BaseModel):
    time_zone_name: str
    opening_hours: List[BusinessOpeningHoursInterval]