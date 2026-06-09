from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from .routers import auth, movies, users, reviews
from .schemas.auth import ApiResponse
from .utils.exceptions import register_exception_handler
from .utils.middleware import register_middleware
from .core.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def life_span(app: FastAPI):
    logger.info("🚀 应用程序启动中... ")
    yield
    logger.info("🏁 应用程序已关闭")


app = FastAPI(lifespan=life_span)


# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(
            code=exc.status_code, message=str(exc.detail), data=None
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    message = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in errors])
    return JSONResponse(
        status_code=422,
        content=ApiResponse(
            code=422, message=f"请求参数校验失败: {message}", data=None
        ).model_dump(),
    )


# 自定义异常处理
register_exception_handler(app)
# 中间件
register_middleware(app)

app.include_router(users.router, prefix="/api/v1/users", tags=["用户"])
app.include_router(movies.router, prefix="/api/v1/movies", tags=["电影"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(reviews.router, prefix="/api/v1/movies", tags=["电影评论"])
