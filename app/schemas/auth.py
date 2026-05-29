import uuid
from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

from app.schemas.movie import MovieOutput

T = TypeVar("T")


# 用户创建模型
class UserCreate(BaseModel):
    username: str = Field(max_length=25)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


# 用户响应模型
class UserOutput(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    username: str = Field(max_length=25)


# 用户登陆模型
class UserLogging(BaseModel):
    username: str = Field(max_length=40)
    password: str = Field(min_length=6)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    new_password: str = Field(min_length=6)
    confirm: str = Field(min_length=6)


class ApiResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "ok"
    data: Optional[T] = None
