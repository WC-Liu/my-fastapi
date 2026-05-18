from typing import Any

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse


# 用户模块
class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class UserDisabledError(Exception):
    pass


# 认证模块
class UnauthorizedError(Exception):
    pass


class TokenExpiredError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class AccessTokenRequired(Exception):
    pass


class RefreshTokenRequired(Exception):
    pass


class PermissionDeniedError(Exception):
    pass


# 电影模块
class MovieNotFoundError(Exception):
    pass


class MovieAlreadyExistsError(Exception):
    pass


# 创建异常处理闭包工厂
def create_exception_handler(status_code: int, detail: Any):
    async def handler(request: Request, exc: Exception):
        return JSONResponse(status_code=status_code, content={"detail": detail})

    return handler


def register_exception_handler(app: FastAPI):
    handlers = {
        UserNotFoundError: (404, "用户不存在"),
        UserAlreadyExistsError: (400, "用户已注册"),
        InvalidPasswordError: (400, "密码错误"),
        UnauthorizedError: (401, "请先登录"),
        TokenExpiredError: (401, "登录已过期，请重新登录"),
        InvalidTokenError: (401, "token错误或者已过期"),
        PermissionDeniedError: (403, "权限不足，非管理员"),
        AccessTokenRequired: (401, "请提供一个token"),
        RefreshTokenRequired: (401, "请提供一个刷新token"),
        MovieNotFoundError: (404, "电影不存在"),
    }
    for exc, (code, msg) in handlers.items():
        app.add_exception_handler(exc, create_exception_handler(code, msg))
