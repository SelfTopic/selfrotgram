from pydantic import BaseModel


class BusinessOpeningHoursInterval(BaseModel):
    opening_minute: int
    closing_minute: int