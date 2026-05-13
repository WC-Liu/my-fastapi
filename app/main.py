from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.db import init_db

from .routers import movies, users


@asynccontextmanager
async def life_span(app: FastAPI):
    print("应用程序启动")
    # await init_db()
    yield
    print("应用程序结束")


app = FastAPI(lifespan=life_span)

app.include_router(movies.router, prefix="/movies", tags=["电影"])
app.include_router(users.router, prefix="/users", tags=["用户"])
