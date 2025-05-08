from pydantic import BaseModel

class UniqueGiftBackdropColors(BaseModel):
    center_color: int
    edge_color: int
    symbol_color: int
    text_color: int