from typing import Optional
from pydantic import BaseModel

class WriteAccessAllowed(BaseModel):
    from_request: Optional[bool] = None
    web_app_name: Optional[str] = None
    from_attachment_menu: Optional[bool] = None