from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate


class MovieService:
    async def get_all_movies(self, session: AsyncSession):
        stmt = select(Movie).order_by(desc(Movie.created_at))
        result = await session.exec(stmt)
        return result.all()

    async def get_user_movies(self, user_uid: str, session: AsyncSession):
        stmt = (
            select(Movie)
            .where(Movie.user_id == user_uid)
            .order_by(desc(Movie.created_at))
        )
        result = await session.exec(stmt)
        return result.all()

    async def get_movie(self, movie_uid: str, session: AsyncSession):
        stmt = select(Movie).where(Movie.uid == movie_uid)
        result = await session.exec(stmt)
        movie = result.first()
        if movie:
            return movie
        else:
            return None

    async def create_movie(
        self, movie_data: MovieCreate, user_uid: str, session: AsyncSession
    ):
        stmt = select(Movie).where(Movie.imdb == movie_data.imdb)
        result = await session.exec(stmt)
        movie = result.first()
        if movie:
            return None
        new_movie = Movie(**movie_data.model_dump())
        new_movie.user_id = user_uid
        session.add(new_movie)
        await session.commit()
        return new_movie

    async def update_movie(
        self, movie_uid: str, movie_data: MovieUpdate, session: AsyncSession
    ):
        movie_to_update = await self.get_movie(movie_uid, session)
        if movie_to_update:
            for field, value in movie_data.model_dump(exclude_unset=True).items():
                setattr(movie_to_update, field, value)
                await session.commit()
            return movie_to_update
        else:
            return None

    async def delete_movie(self, movie_uid: str, session: AsyncSession):
        movie_to_delete = await self.get_movie(movie_uid, session)
        if movie_to_delete:
            await session.delete(movie_to_delete)
            await session.commit()
            return True
        else:
            return None


movie_service = MovieService()
