from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import (
    DUMMY_HASH,
    REFRESH_TOKEN_EXPIRY,
    create_access_token,
    decode_token,
    generate_passwd_hash,
    verify_password,
)
from app.db.redis import add_jti_to_blacklist, token_in_blacklist
from app.models.models import User
from app.schemas.auth import Token, UserCreate
from app.utils import exceptions

from .user_service import user_service


class AuthService:
    # 创建用户
    async def create_user(self, user_data: UserCreate, session: AsyncSession) -> User:
        new_user = User(**(user_data.model_dump()))
        try:
            user = await user_service.get_user_by_email(new_user.email, session)
            if user:
                raise exceptions.UserAlreadyExistsError()
        except exceptions.UserNotFoundError:
            pass
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
    async def refresh_access_token(self, token: str) -> dict:
        token_details = decode_token(token)
        if token_details is None:
            raise exceptions.InvalidTokenError()
        if not token_details["refresh"]:
            raise exceptions.RefreshTokenRequired()
        jti = token_details.get("jti")

        if jti and await token_in_blacklist(jti):
            raise exceptions.TokenInBlacklist()
        exp_dt = datetime.fromtimestamp(token_details["exp"], tz=timezone.utc)
        now_dt = datetime.now(timezone.utc)
        if exp_dt > now_dt:
            new_access_token = create_access_token(subject=token_details["sub"])
            new_refresh_token = create_access_token(
                subject=token_details["sub"],
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )
            if token_details.get("jti"):
                await add_jti_to_blacklist(token_details["jti"])
            return {
                "new_access_token": new_access_token,
                "new_refresh_token": new_refresh_token,
            }

        raise exceptions.TokenExpiredError()

    async def logout_user(self, token: str) -> None:
        token_details = decode_token(token)
        jti = token_details["jti"]
        await add_jti_to_blacklist(jti)


auth_service = AuthService()
