import uuid
from datetime import datetime
from typing import Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel


# 电影评论数据库表
class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, default=uuid.uuid4, primary_key=True, nullable=False)
    )
    rating: float = Field(ge=0, le=10)
    review_text: str
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    movie_id: Optional[uuid.UUID] = Field(default=None, foreign_key="movies.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )
    user: Optional["User"] = Relationship(back_populates="reviews")
    movie: Optional["Movie"] = Relationship(back_populates="reviews")
