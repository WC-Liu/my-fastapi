from typing import List
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.dependencies import CurrentUser, SessionDep
from app.schemas.review import ReviewCreate, ReviewOutput
from app.service.review_service import ReviewService

from .movies import router

review_service = ReviewService()


@router.post("/{movie_uid}/reviews")
async def add_review_to_movies(
    movie_uid: str,
    review_data: ReviewCreate,
    current_user: CurrentUser,
    session: SessionDep,
):
    new_review = await review_service.add_review_to_movie(
        user_email=current_user.email,
        movie_uid=movie_uid,
        review_data=review_data,
        session=session,
    )
    return new_review


@router.get("/{movie_uid}/reviews")
async def get_movie_reviews(movie_uid: UUID, session: SessionDep):
    reviews = await review_service.get_movie_all_reviews(movie_uid, session)
    return reviews


@router.delete("/{movie_uid}/reviews/{review_uid}")
async def delete_user_review(
    current_user: CurrentUser, movie_uid: UUID, review_uid: UUID, session: SessionDep
):

    await review_service.delete_user_review(
        current_user.uid, movie_uid, review_uid, session
    )
