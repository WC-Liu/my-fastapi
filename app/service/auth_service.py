from datetime import timedelta

from fastapi.responses import JSONResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import create_access_token, generate_passwd_hash, verify_password
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogging

REFRESH_TOKEN_EXPIRY = 2


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
        new_user.role = "user"
        session.add(new_user)
        await session.commit()
        return new_user

    async def login_user(self, login_data: UserLogging, session: AsyncSession):
        email = login_data.email
        password = login_data.password
        user = await self.get_user_by_email(email, session)
        if user is not None:
            if verify_password(password, user.password_hashed):
                access_token = create_access_token(
                    user_data={
                        "email": user.email,
                        "user_uid": str(user.uid),
                        "role": user.role,
                    }
                )

                refresh_token = create_access_token(
                    user_data={"email": user.email, "user_uid": str(user.uid)},
                    refresh=True,
                    expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
                )
                return {
                    "message": "登录成功",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "user_uid": str(user.uid)},
                }
        return None


user_service = UserService()
