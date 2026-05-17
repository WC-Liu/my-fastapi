from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from .routers import auth, movies, reviews, users
from .utils import exceptions


@asynccontextmanager
async def life_span(app: FastAPI):
    print("应用程序启动")
    # await init_db()
    yield
    print("应用程序结束")


app = FastAPI(lifespan=life_span)


@app.exception_handler(exceptions.UserNotFoundError)
async def user_not_found(request: Request, exc: exceptions.UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": "用户不存在"}
    )


@app.exception_handler(exceptions.UserAlreadyExistsError)
def user_exists(request: Request, exc: exceptions.UserAlreadyExistsError):
    return JSONResponse(status_code=400, content={"detail": "用户已注册"})


@app.exception_handler(exceptions.InvalidPasswordError)
def invalid_pw(request: Request, exc: exceptions.InvalidPasswordError):
    return JSONResponse(status_code=400, content={"detail": "密码错误"})


@app.exception_handler(exceptions.UnauthorizedError)
def unauthorized(request: Request, exc: exceptions.UnauthorizedError):
    return JSONResponse(status_code=401, content={"detail": "请先登录"})


@app.exception_handler(exceptions.TokenExpiredError)
def token_expired(request: Request, exc: exceptions.TokenExpiredError):
    return JSONResponse(status_code=401, content={"detail": "登录已过期，请重新登录"})


@app.exception_handler(exceptions.InvalidTokenError)
def invalid_token(request: Request, exc: exceptions.InvalidTokenError):
    return JSONResponse(status_code=401, content={"detail": "token错误或者已过期"})


@app.exception_handler(exceptions.PermissionDeniedError)
def no_permission(request: Request, exc: exceptions.PermissionDeniedError):
    return JSONResponse(status_code=403, content={"detail": "权限不足，非管理员"})


@app.exception_handler(exceptions.AccessTokenRequired)
def access_token(request: Request, exc: exceptions.AccessTokenRequired):
    return JSONResponse(status_code=401, content={"detail": "请提供一个token"})


@app.exception_handler(exceptions.RefreshTokenRequired)
def refresh_token(request: Request, exc: exceptions.RefreshTokenRequired):
    return JSONResponse(status_code=401, content={"detail": "请提供一个刷新token"})


@app.exception_handler(exceptions.MovieNotFoundError)
def movie_not_found(request: Request, exc: exceptions.MovieNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "电影不存在"})


app.include_router(users.router, prefix="/api/v1/users", tags=["用户"])
app.include_router(movies.router, prefix="/api/v1/movies", tags=["电影"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["用户"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["电影评论"])
