from datetime import datetime, timedelta

from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import (
    DUMMY_HASH,
    create_access_token,
    decode_token,
    generate_passwd_hash,
    verify_password,
)
from app.db.redis import add_jti_to_blacklist, token_in_blacklist
from app.models.models import User
from app.schemas.auth import UserCreate
from app.utils import exceptions

from .user_service import user_service

REFRESH_TOKEN_EXPIRY = 2


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthService:
    # 创建用户
    async def create_user(self, user_data: UserCreate, session: AsyncSession) -> User:
        new_user = User(**(user_data.model_dump()))
        user = await user_service.get_user_by_email(new_user.email, session)
        if user:
            raise exceptions.UserAlreadyExistsError()
        new_user.password_hashed = generate_passwd_hash(user_data.password)

        session.add(new_user)
        await session.commit()
        return new_user

    # 用户登陆，获取双令牌
    async def login_user(
        self, login_data: OAuth2PasswordRequestForm, session: AsyncSession
    ) -> Token:
        email = login_data.username
        password = login_data.password
        user = await user_service.get_user_by_email(email, session)
        if not user:
            verify_password(password, DUMMY_HASH)
            raise exceptions.UserNotFoundError()
        if not verify_password(password, user.password_hashed):
            raise exceptions.InvalidPasswordError()
        access_token = create_access_token(user.uid)
        refresh_token = create_access_token(
            user.uid,
            refresh=True,
            expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
        )
        return Token(access_token=access_token, refresh_token=refresh_token)

    # 刷新令牌
    async def refresh_access_token(self, token: str):
        token_details = decode_token(token)
        if token_details is None:
            raise exceptions.InvalidTokenError()
        if not token_details["refresh"]:
            raise exceptions.RefreshTokenRequired()
        expired_token = await token_in_blacklist(token_details["jti"])
        if expired_token:
            raise exceptions.TokenInBlacklist()
        if datetime.fromtimestamp(token_details["exp"]) > datetime.now():
            new_access_token = create_access_token(subject=token_details["sub"])
            new_refresh_token = create_access_token(
                subject=token_details["sub"],
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )
            await add_jti_to_blacklist(token_details["jti"])
            return JSONResponse(
                content={
                    "new_access_token": new_access_token,
                    "new_refresh_token": new_refresh_token,
                }
            )
        raise exceptions.TokenExpiredError()


auth_service = AuthService()
