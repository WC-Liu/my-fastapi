from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.models import Review
from app.schemas.review import ReviewCreate
from app.service.auth_service import user_service
from app.service.movie_service import movie_service


class ReviewService:
    async def get_all_review(self, session: AsyncSession):
        stmt = select(Review).options(
            selectinload(Review.user), selectinload(Review.movie)
        )
        result = await session.exec(stmt)
        return result.all()

    async def add_review_to_movie(
        self,
        user_email: str,
        movie_uid: str,
        review_data: ReviewCreate,
        session: AsyncSession,
    ):
        try:
            movie = await movie_service.get_movie(movie_uid, session)
            user = await user_service.get_user_by_email(user_email, session)
            new_review = Review(**review_data.model_dump())
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="电影不存在"
                )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
                )

            new_review.user = user
            new_review.movie = movie
            session.add(new_review)
            await session.commit()
            return new_review

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="出错了"
            )

    async def delete_user_review(
        self, user_email: str, movie_uid: str, review_uid: str, session: AsyncSession
    ):
        pass
