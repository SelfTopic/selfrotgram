from pydantic import BaseModel

class PreparedInlineMessage(BaseModel):
    id: str
    expiration_date: int