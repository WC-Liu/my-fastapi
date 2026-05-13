import uuid
from datetime import datetime
from typing import Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


# 公共字段
class MovieBase(SQLModel):
    title: str
    director: str
    year: int
    rating: float = Field(..., ge=0, le=10)
    genre: str
    is_showing: bool = Field(default=False)
    imdb: str


# 数据库模型
class Movie(MovieBase, table=True):
    __tablename__ = "movies"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, default=uuid.uuid4, primary_key=True, nullable=False)
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )


# 创建请求
class MovieCreate(MovieBase):
    pass


# 更新请求
class MovieUpdate(SQLModel):
    title: Optional[str] = None
    director: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = Field(None, ge=0, le=10)
    genre: Optional[str] = None
    is_showing: Optional[bool] = False


# 响应模型
class MovieOutput(SQLModel):
    uid: uuid.UUID
    title: str
    director: str
    year: int
    rating: float
    genre: str
    is_showing: bool
    imdb: str
    created_at: datetime
    updated_at: datetime


def __repr__(self):
    return f"<Movie {self.title}>"
