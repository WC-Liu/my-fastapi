from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    rating: float = Field(ge=0, le=10)
    review_text: str


class ReviewOutput(BaseModel):
    uid: UUID
    rating: float = Field(ge=0, le=10)
    review_text: str
    user_id: UUID | None = None
    movie_id: UUID | None = None
    created_at: datetime
