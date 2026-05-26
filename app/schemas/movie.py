import uuid
from datetime import datetime
from typing import List, Optional

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
    title: Optional[str] = None
    director: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = Field(None, ge=0, le=10)
    genre: Optional[str] = None
    is_showing: Optional[bool] = False


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
    user_id: uuid.UUID | None = None
    created_at: datetime


class MovieReviewOutPut(MovieOutput):
    reviews: List[ReviewOutput]
