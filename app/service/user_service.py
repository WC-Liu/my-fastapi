from typing import List
from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.models import Movie, User
from app.schemas.auth import UserUpdate
from app.utils import exceptions


class UserService:
    async def get_all_users(self, session: AsyncSession) -> List[Movie]:
        stmt = select(User).order_by(desc(User.created_at))
        result = await session.exec(stmt)
        return result.all()

    async def get_user_by_email(self, email: str, session: AsyncSession) -> User:
        stmt = select(User).where(User.email == email)
        result = await session.exec(stmt)
        user = result.first()
        if not user:
            raise exceptions.UserNotFoundError()
        return user

    async def get_user_by_user_uid(self, user_uid: UUID, session: AsyncSession) -> User:
        stmt = select(User).where(User.uid == user_uid)
        result = await session.exec(stmt)
        user = result.first()
        if user is None:
            raise exceptions.UserNotFoundError()
        return user

    async def update_user(
        self, user_uid: UUID, user_update: UserUpdate, session: AsyncSession
    ) -> User:
        user = await self.get_user_by_user_uid(user_uid, session)
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await session.commit()
        return user

    async def delete_user(self, user_uid: UUID, session: AsyncSession) -> None:
        user = await self.get_user_by_user_uid(user_uid, session)
        await session.delete(user)
        await session.commit()


user_service = UserService()
