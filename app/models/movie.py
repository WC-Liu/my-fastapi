import uuid
from datetime import datetime
from typing import Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class Movie(SQLModel, table=True):
    __tablename__ = "movies"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, default=uuid.uuid4, primary_key=True, nullable=False)
    )
    title: str
    director: str
    year: int
    rating: float = Field(..., ge=0, le=10)
    genre: str
    is_showing: bool = Field(default=False)
    imdb: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )
