import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from .review import ReviewOutput


# 创建请求
class MovieCreate(BaseModel):
    title: str
    director: str
    year: int
    rating: float = Field(..., ge=0, le=10)
    genre: str
    is_showing: bool = Field(default=False)
    imdb: str


# 更新请求
class MovieUpdate(BaseModel):
    title: str | None= None
    director: str | None = None
    year: int | None= None
    rating: float | None = Field(None, ge=0, le=10)
    genre: str | None = None
    is_showing: bool | None = None


# 响应模型
class MovieOutput(BaseModel):
    uid: uuid.UUID
    title: str
    director: str
    year: int
    rating: float
    genre: str
    is_showing: bool
    imdb: str
    created_at: datetime


class MovieReviewOutPut(MovieOutput):
    reviews: list[ReviewOutput]
