from pydantic import BaseModel

class StoryAreaPosition(BaseModel):
    x_percentage: float
    y_percentage: float
    width_percentage: float
    height_percentage: float
    rotation_angle: float
    corner_radius_percentage: float