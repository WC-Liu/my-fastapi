from typing import List

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.db import get_session
from app.db.redis import token_in_blacklist
from app.models.user import User
from app.service.auth_service import user_service
from app.utils import exceptions

from .security import decode_token


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(
            auto_error=auto_error
        )  # super(): python内置方法，调用父类的方法，初始化父类

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        # 调用父类获取HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)并存到creds
        creds = await super().__call__(request)

        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise exceptions.InvalidTokenError()
        if await token_in_blacklist(token_data["jti"]):
            raise exceptions.InvalidTokenError()

        self.verify_token_data(token_data)
        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        if token_data:
            return True
        else:
            return False

    def verify_token_data(self, token_data):
        raise NotImplementedError("请在子类覆盖此方法")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data and token_data["refresh"]:
            raise exceptions.AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data and not token_data["refresh"]:
            raise exceptions.RefreshTokenRequired()


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_details["user"]["email"]
    user = await user_service.get_user_by_email(user_email, session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True

        raise exceptions.PermissionDeniedError()
