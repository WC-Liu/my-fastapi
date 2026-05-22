import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.schemas.movie import MovieOutput


# 用户创建模型
class UserCreate(BaseModel):
    username: str = Field(max_length=10)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


# 用户响应模型
class UserOutput(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserMoviesOutput(UserOutput):
    movies: List[MovieOutput]


class UserUpdate(BaseModel):
    username: str = Field(max_length=10)


# 用户登陆模型
class UserLogging(BaseModel):
    username: str = Field(max_length=40)
    password: str = Field(min_length=6)


class Email(BaseModel):
    emails: List[str]


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    new_password: str = Field(min_length=6)
    confirm: str = Field(min_length=6)
