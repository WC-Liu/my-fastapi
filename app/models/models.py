import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import DateTime, event
from sqlmodel import Field, Relationship, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


# 用户数据库模型
class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    password_hashed: str
    email: str
    is_superuser: bool = False
    is_active: bool = False
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc, sa_type=DateTime(timezone=True)
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc, sa_type=DateTime(timezone=True)
    )
    movies: List["Movie"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )


# 电影数据库模型
class Movie(SQLModel, table=True):
    __tablename__ = "movies"
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    director: str
    year: int
    rating: float = Field(..., ge=0, le=10)
    genre: str
    is_showing: bool = Field(default=False)
    imdb: str
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc, sa_type=DateTime(timezone=True)
    )
    user: Optional["User"] = Relationship(back_populates="movies")
    reviews: List["Review"] = Relationship(
        back_populates="movie", sa_relationship_kwargs={"lazy": "selectin"}
    )


# 电影评论数据库模型
class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    rating: float = Field(ge=0, le=10)
    review_text: str
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    movie_id: Optional[uuid.UUID] = Field(default=None, foreign_key="movies.uid")
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc, sa_type=DateTime(timezone=True)
    )
    user: Optional["User"] = Relationship(back_populates="reviews")
    movie: Optional["Movie"] = Relationship(back_populates="reviews")


@event.listens_for(User, "before_update")
def receive_before_update(mapper, connection, target):
    target.updated_at = get_datetime_utc()
