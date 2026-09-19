from typing import Optional

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert(
        self,
        telegram_id: int,
        first_name: str,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
    ) -> User:
        stmt = (
            insert(User)
            .values(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            .on_conflict_do_update(
                index_elements=["telegram_id"],
                set_={
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                },
            )
            .returning(User)
        )

        user = await self.session.scalar(stmt)
        if user is None:
            raise RuntimeError(f"User {telegram_id} not found after upsert")

        return user
