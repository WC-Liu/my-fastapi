from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    RoleChecker,
    get_current_user,
)
from app.db.db import get_session
from app.db.redis import add_jti_to_blacklist
from app.schemas.auth import (
    Email,
    PasswordResetConfirm,
    PasswordResetRequest,
    UserCreate,
    UserLogging,
    UserMoviesOutput,
    UserOutput,
)
from app.service.auth_service import auth_service
from app.service.mail_service import mail_service

# 刷新令牌过期时间
REFRESH_TOKEN_EXPIRY = 2
rolechecker = RoleChecker(["admin", "user"])
access_token_bearer = AccessTokenBearer()
refreshtokenbearer = RefreshTokenBearer()

router = APIRouter()


# 创建新用户
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    new_user = await auth_service.create_user(user_data, session)

    await mail_service.send_verify_email(user_data.email)

    return {"message": "账号已创建", "user": new_user}


@router.get("/verify/{email_token}")
async def verify_user_account(
    email_token: str, session: AsyncSession = Depends(get_session)
):
    return await mail_service.verified_user(email_token, {"is_verified": True}, session)


# 用户登陆
@router.post("/login")
async def login_user(
    login_data: UserLogging, session: AsyncSession = Depends(get_session)
):
    result = await auth_service.login_user(login_data, session)
    return result


# 刷新令牌
@router.get("/refresh")
async def get_new_access_token(token_details: dict = Depends(refreshtokenbearer)):
    return await auth_service.refresh_access_token(token_details)


# 退出登录
@router.get("/logout")
async def revoke_token(token_details: dict = Depends(access_token_bearer)):
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
    session: AsyncSession = Depends(get_session),
):
    return await mail_service.reset_password(email_token, passwords, session)


@router.get("/me", response_model=UserMoviesOutput)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(rolechecker)
):
    return user
