from typing import List
from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.models import Movie
from app.schemas.movie import MovieCreate, MovieUpdate
from app.utils import exceptions


class MovieService:
    async def get_all_movies(self, session: AsyncSession) -> List[Movie]:
        stmt = select(Movie).order_by(desc(Movie.created_at))
        result = await session.exec(stmt)
        return result.all()

    async def get_movie(self, movie_uid: UUID, session: AsyncSession) -> Movie:
        stmt = select(Movie).where(Movie.uid == movie_uid)
        result = await session.exec(stmt)
        movie = result.first()
        if not movie:
            raise exceptions.MovieNotFoundError()
        return movie

    async def create_movie(
        self, movie_data: MovieCreate, session: AsyncSession
    ) -> Movie:
        stmt = select(Movie).where(Movie.imdb == movie_data.imdb)
        result = await session.exec(stmt)
        movie = result.first()
        if movie:
            raise exceptions.MovieAlreadyExistsError()
        new_movie = Movie(**movie_data.model_dump())
        session.add(new_movie)
        await session.commit()
        return new_movie

    async def update_movie(
        self, movie_uid: UUID, movie_data: MovieUpdate, session: AsyncSession
    ) -> Movie:
        movie_to_update = await self.get_movie(movie_uid, session)
        for field, value in movie_data.model_dump(exclude_unset=True).items():
            setattr(movie_to_update, field, value)
            await session.commit()
        return movie_to_update

    async def delete_movie(self, movie_uid: UUID, session: AsyncSession) -> None:
        movie_to_delete = await self.get_movie(movie_uid, session)
        await session.delete(movie_to_delete)
        await session.commit()


movie_service = MovieService()
