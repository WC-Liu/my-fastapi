from datetime import datetime, timedelta

from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import (
    DUMMY_HASH,
    create_access_token,
    generate_passwd_hash,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogging
from app.utils import exceptions

from .user_service import user_service

REFRESH_TOKEN_EXPIRY = 2


class AuthService:
    # 创建用户
    async def create_user(self, user_data: UserCreate, session: AsyncSession):
        new_user = User(**(user_data.model_dump()))
        user = await user_service.get_user_by_email(new_user.email, session)
        if user:
            raise exceptions.UserAlreadyExistsError()
        new_user.password_hashed = generate_passwd_hash(user_data.password)
        new_user.role = "user"
        session.add(new_user)
        await session.commit()
        return new_user

    # 用户登陆，获取双令牌
    async def login_user(self, login_data: UserLogging, session: AsyncSession):
        email = login_data.email
        password = login_data.password
        user = await user_service.get_user_by_email(email, session)
        if not user:
            verify_password(password, DUMMY_HASH)
            raise exceptions.UserNotFoundError()
        if not verify_password(password, user.password_hashed):
            raise exceptions.InvalidPasswordError()
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

    async def refresh_access_token(self, token_details: dict):
        expiry_timestamp = token_details["exp"]
        if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
            new_access_token = create_access_token(user_data=token_details["user"])
            return JSONResponse(content={"new_access_token": new_access_token})
        raise exceptions.TokenExpiredError()


auth_service = AuthService()
