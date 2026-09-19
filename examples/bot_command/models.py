from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
