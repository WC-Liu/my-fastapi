import uuid
from datetime import datetime
from typing import List

from sqlmodel import Field, SQLModel

from app.schemas.movie import MovieOutput


# 用户创建模型
class UserCreate(SQLModel):
    username: str = Field(max_length=10)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    name: str = Field(max_length=20)


# 用户响应模型
class UserOutput(SQLModel):
    uid: uuid.UUID
    username: str
    email: str
    name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    # movies: List[MovieOutput]
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    }


class UserMoviesOutput(UserOutput):
    movies: List[MovieOutput]


class UserUpdate(SQLModel):
    username: str = Field(max_length=10)
    name: str = Field(max_length=20)


# 用户登陆模型
class UserLogging(SQLModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class Email(SQLModel):
    emails: List[str]
