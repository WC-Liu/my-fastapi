from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.dependencies import (
    CurrentUser,
    SessionDep,
    TokenDep,
    get_current_active_superuser,
    get_current_user,
)
from app.core.security import decode_token
from app.db.redis import add_jti_to_blacklist
from app.schemas.auth import (
    PasswordResetConfirm,
    PasswordResetRequest,
    UserCreate,
    UserMoviesOutput,
    UserOutput,
)
from app.service.auth_service import auth_service
from app.service.mail_service import mail_service

# 刷新令牌过期时间
REFRESH_TOKEN_EXPIRY = 2
current_user = CurrentUser()
router = APIRouter()


class RefreshToken(BaseModel):
    refresh_token: str


# 创建新用户
@router.post(
    "/register", response_model=UserOutput, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data: UserCreate,
    session: SessionDep,
):
    new_user = await auth_service.create_user(user_data, session)

    await mail_service.send_verify_email(user_data.email)

    return new_user


@router.get("/verify/{email_token}")
async def active_user_account(email_token: str, session: SessionDep):
    return await mail_service.actived_user(email_token, {"is_active": True}, session)


# 用户登陆
@router.post("/login")
async def login_user(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    result = await auth_service.login_user(login_data, session)
    return result


# 刷新令牌
@router.post("/refresh")
async def get_new_access_token(refresh_token: RefreshToken):
    return await auth_service.refresh_access_token(refresh_token.refresh_token)


# 退出登录
@router.get("/logout", dependencies=[Depends(get_current_user)])
async def revoke_token(token: TokenDep) -> JSONResponse:
    token_details = decode_token(token)
    jti = token_details["jti"]
    await add_jti_to_blacklist(jti)

    return JSONResponse(
        content={
            "message": "已成功注销",
        },
        status_code=status.HTTP_200_OK,
    )


@router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequest):
    await mail_service.password_reset(email_data.email)
    return JSONResponse(
        content={"message": "请检查你的邮箱并重置你的密码"}, status_code=200
    )


@router.post("/password-reset-confirm/{email_token}")
async def reset_password(
    email_token: str,
    passwords: PasswordResetConfirm,
    session: SessionDep,
):
    return await mail_service.reset_password(email_token, passwords, session)


@router.get("/me", response_model=UserOutput)
async def get_current_user(user: CurrentUser):
    return user
