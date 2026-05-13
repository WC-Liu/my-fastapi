import uuid
from datetime import datetime

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


# 数据库模型
class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, default=uuid.uuid4, primary_key=True, nullable=False)
    )
    username: str
    password_hashd: str = Field(exclude=False)
    email: str
    name: str
    is_verified: bool = False
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    }


# 用户创建模型
class UserCreate(SQLModel):
    username: str = Field(max_length=10)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    name: str = Field(max_length=20)


class UserOutput(SQLModel):
    uid: uuid.UUID
    username: str
    password_hashd: str = Field(exclude=True)
    email: str
    name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    }
