from typing import List
from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.models import Review
from app.schemas.review import ReviewCreate
from app.service.auth_service import user_service
from app.service.movie_service import movie_service
from app.utils import exceptions


class ReviewService:
    async def get_movie_all_reviews(
        self, movie_uid: UUID, session: AsyncSession
    ) -> List[Review]:
        await movie_service.get_movie(movie_uid, session)
        stmt = select(Review).where(Review.movie_id == movie_uid)
        results = await session.exec(stmt)
        reviews = results.all()
        if reviews is None:
            raise HTTPException(status_code=404, detail="不存在")
        return reviews

    async def add_review_to_movie(
        self,
        user_email: str,
        movie_uid: UUID,
        review_data: ReviewCreate,
        session: AsyncSession,
    ):

        movie = await movie_service.get_movie(movie_uid, session)
        user = await user_service.get_user_by_email(user_email, session)
        new_review = Review(**review_data.model_dump())
        new_review.user = user
        new_review.movie = movie
        session.add(new_review)
        await session.commit()
        return new_review

    async def get_review(self, review_uid: UUID, session: AsyncSession) -> Review:
        stmt = select(Review).where(Review.uid == review_uid)
        result = await session.exec(stmt)
        review = result.first()
        if review is None:
            raise HTTPException(status_code=404, detail="不存在")
        return review

    async def delete_user_review(
        self, user_uid: UUID, movie_uid: UUID, review_uid: str, session: AsyncSession
    ) -> None:
        await user_service.get_user_by_user_uid(user_uid, session)
        await movie_service.get_movie(movie_uid, session)
        review = await self.get_review(review_uid, session)
        await session.delete(review)
        await session.commit()


review_service = ReviewService()
