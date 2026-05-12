from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from typing import Optional
import uuid


# 公共字段
class MovieBase(SQLModel):
    title: str
    director: str
    year: int
    rating: float = Field(..., ge=0, le=10)
    genre: str
    is_showing: bool = False


# 数据库模型
class Movie(MovieBase, table=True):
    __tablename__ = "movies"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )

    class Config:
        json_encoders = {datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}


# 响应模型
# class MovieOutput(Movie):
#    pass


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


def __repr__(self):
    return f"<Movie {self.title}>"
