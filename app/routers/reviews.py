from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.dependencies import get_current_user
from app.db.db import get_session
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewOutput
from app.service.review_service import ReviewService

router = APIRouter()
review_service = ReviewService()


@router.post("/movies/{movie_uid}")
async def add_review_to_movies(
    movie_uid: str,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    new_review = await review_service.add_review_to_movie(
        user_email=current_user.email,
        movie_uid=movie_uid,
        review_data=review_data,
        session=session,
    )
    return new_review


@router.get("movies/")
@router.delete("/movie/{movie_uid}/{review_uid}")
async def delete_user_review():
    pass
