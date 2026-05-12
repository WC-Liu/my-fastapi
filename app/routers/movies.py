from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from ..schemas.movie import Movie, MovieCreate, MovieUpdate
from app.service.movie_service import movie_service
from app.db.db import get_session
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Movie])
async def get_movies(session: AsyncSession = Depends(get_session)):
    movies = await movie_service.get_all_movies(session)
    return movies


@router.get("/{movie_uid}", response_model=Movie)
async def get_movie(movie_uid: str, session: AsyncSession = Depends(get_session)):
    movie = await movie_service.get_movie(movie_uid, session)
    if movie:
        return movie
    else:
        raise HTTPException(status_code=404, detail=f"电影 ID {movie_uid} 不存在")


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
async def create_movie(
    movie_data: MovieCreate, session: AsyncSession = Depends(get_session)
):
    new_movie = await movie_service.create_movie(movie_data, session)
    return new_movie


@router.patch("/{movie_uid}", response_model=Movie)
async def update_movie(
    movie_uid: str,
    movie_update: MovieUpdate,
    session: AsyncSession = Depends(get_session),
):
    updated_movie = await movie_service.update_movie(movie_uid, movie_update, session)
    if updated_movie:
        return updated_movie
    else:
        raise HTTPException(status_code=404, detail=f"电影 id{movie_uid}不存在")


@router.delete("/{movie_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_uid: str, session: AsyncSession = Depends(get_session)):
    deleted_movie = await movie_service.delete_movie(movie_uid, session)
    if deleted_movie:
        return "用户已经删除"
    else:
        raise HTTPException(status_code=404, detail=f"电影 ID {movie_uid} 不存在")
