from typing import Optional
from pydantic import BaseModel

class InputProfilePhotoAnimated(BaseModel):
    type: str
    animation: str
    main_frame_timestamp: Optional[float] = None