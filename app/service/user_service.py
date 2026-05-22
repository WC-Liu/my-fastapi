from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.models import Movie, User
from app.schemas.auth import UserUpdate
from app.utils import exceptions


class UserService:
    # 获取所有用户
    async def get_all_users(self, session: AsyncSession):
        stmt = select(User).order_by(desc(User.created_at))
        result = await session.exec(stmt)
        return result.all()

    # 通过邮件查询用户
    async def get_user_by_email(self, email: str, session: AsyncSession):
        stmt = select(User).where(User.email == email)
        result = await session.exec(stmt)
        if not result:
            raise exceptions.UserNotFoundError()
        return result.first()

    # 通过用户uid查询用户
    async def get_user_by_user_uid(self, user_uid: str, session: AsyncSession):
        stmt = select(User).where(User.uid == user_uid)
        result = await session.exec(stmt)
        return result.first()

    # 修改用户信息
    async def update_user(
        self, user_uid: str, user_update: UserUpdate, session: AsyncSession
    ):
        user = await self.get_user_by_user_uid(user_uid, session)
        if not user:
            return False
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
            await session.commit()
        return user

    # 删除用户
    async def delete_user(self, user_uid: str, session: AsyncSession):
        user = await self.get_user_by_user_uid(user_uid, session)
        if not user:
            return False
        await session.delete(user)
        await session.commit()
        return True

    async def get_user_movies(self, user_uid: str, session: AsyncSession):
        stmt = (
            select(Movie)
            .where(Movie.user_id == user_uid)
            .order_by(desc(Movie.created_at))
        )
        result = await session.exec(stmt)
        return result.all()


user_service = UserService()
