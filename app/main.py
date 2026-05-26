from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routers import auth, movies, reviews, users
from .utils.exceptions import register_exception_handler
from .utils.middleware import register_middleware


@asynccontextmanager
async def life_span(app: FastAPI):
    print("应用程序启动")
    yield
    print("应用程序结束")


app = FastAPI(lifespan=life_span)

register_exception_handler(app)
register_middleware(app)

app.include_router(users.router, prefix="/api/v1/users", tags=["用户"])
app.include_router(movies.router, prefix="/api/v1/movies", tags=["电影"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
# app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["电影评论"])
