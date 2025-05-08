from pydantic import BaseModel

class StoryAreaTypeWeather(BaseModel):
    type: str
    temperature: float
    emoji: str
    background_color: int