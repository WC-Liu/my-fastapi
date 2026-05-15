import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: str | None = None


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
    # password_hashed: str = Field(exclude=True)
    email: str
    name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    }


# 用户登陆模型
class UserLogging(SQLModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
