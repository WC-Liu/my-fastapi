import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ReviewCreate(SQLModel):
    rating: float = Field(ge=0, le=10)
    review_text: str


class ReviewOutput(SQLModel):
    uid: uuid.UUID
    rating: float = Field(ge=0, le=10)
    review_text: str
    user_id: Optional[uuid.UUID]
    movie_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_encoders": {datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    }
