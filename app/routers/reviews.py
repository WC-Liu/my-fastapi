from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.dependencies import CurrentUser, SessionDep, get_current_user
from app.models.models import Review
from app.schemas.auth import ApiResponse
from app.schemas.review import ReviewCreate
from app.service.review_service import review_service

router = APIRouter()


@router.post("/{movie_uid}/reviews")
async def add_review_to_movies(
    movie_uid: UUID,
    review_data: ReviewCreate,
    current_user: CurrentUser,
    session: SessionDep,
) -> ApiResponse[Review]:
    new_review = await review_service.add_review_to_movie(
        user_email=current_user.email,
        movie_uid=movie_uid,
        review_data=review_data,
        session=session,
    )
    return ApiResponse(data=new_review)


@router.get("/{movie_uid}/reviews", dependencies=[Depends(get_current_user)])
async def get_movie_reviews(
    movie_uid: UUID, session: SessionDep
) -> ApiResponse[List[Review]]:
    reviews = await review_service.get_movie_all_reviews(movie_uid, session)
    return ApiResponse(data=reviews)


@router.delete(
    "/{movie_uid}/reviews/{review_uid}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user_review(
    current_user: CurrentUser, movie_uid: UUID, review_uid: UUID, session: SessionDep
) -> None:

    await review_service.delete_user_review(
        current_user.uid, movie_uid, review_uid, session
    )
