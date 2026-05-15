from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.models.user import User

# 创建数据库引擎
async_engine = AsyncEngine(create_engine(url=settings.DATABASE_URL, echo=True))


# 创建会话工厂
async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with Session() as session:
        yield session
