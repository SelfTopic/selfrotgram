from pydantic import BaseModel

class InputProfilePhotoStatic(BaseModel):
    type: str
    photo: str