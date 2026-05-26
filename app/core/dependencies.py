from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.db import get_session
from app.db.redis import token_in_blacklist
from app.models.models import User
from app.service.auth_service import user_service
from app.utils import exceptions

from .security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(
    token: TokenDep,
    session: SessionDep,
) -> User:
    token_details = decode_token(token)
    if not token_details:
        raise exceptions.InvalidTokenError()
    user_uid = token_details["sub"]
    user = await user_service.get_user_by_user_uid(user_uid, session)
    expired_token = await token_in_blacklist(token_details["jti"])
    if expired_token:
        raise exceptions.TokenInBlacklist()
    if not user:
        raise exceptions.UserNotFoundError()
    if not user.is_active:
        raise exceptions.AccountNotActived()
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="用户权限不足")
    return current_user
