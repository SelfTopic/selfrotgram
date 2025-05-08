from pydantic import BaseModel

class TransactionPartnerTelegramApi(BaseModel):
    type: str
    request_count: int