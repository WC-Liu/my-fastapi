import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    rating: float = Field(ge=0, le=10)
    review_text: str


class ReviewOutput(BaseModel):
    uid: uuid.UUID
    rating: float = Field(ge=0, le=10)
    review_text: str
    user_id: Optional[uuid.UUID]
    movie_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime
