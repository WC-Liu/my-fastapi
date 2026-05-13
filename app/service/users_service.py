from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import generate_passwd_hash, verify_password
from app.schemas.user import User, UserCreate


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()

        return user

    async def user_exiests(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreate, session: AsyncSession):
        new_user = User(**(user_data.model_dump()))
        new_user.password_hashd = generate_passwd_hash(user_data.password)
        session.add(new_user)
        await session.commit()
        return new_user


user_service = UserService()
