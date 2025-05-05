from pydantic import BaseModel


class InputStoryContentPhoto(BaseModel):
    type: str
    photo: str