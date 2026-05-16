from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.dependencies import AccessTokenBearer, RoleChecker
from app.db.db import get_session
from app.service.movie_service import movie_service

from ..schemas.movie import MovieCreate, MovieOutput, MovieUpdate

access_token_bearer = AccessTokenBearer()
rolechecker = RoleChecker(["admin", "user"])
router = APIRouter(dependencies=[Depends(rolechecker)])


@router.get("/", response_model=List[MovieOutput])
async def get_movies(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    movies = await movie_service.get_all_movies(session)
    return movies


@router.get("/user/{user_uid}", response_model=List[MovieOutput])
async def get_user_movie_sub(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_dedails: dict = Depends(access_token_bearer),
):
    movies = await movie_service.get_user_movies(user_uid, session)
    return movies


@router.get("/{movie_uid}", response_model=MovieOutput)
async def get_movie(
    movie_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    movie = await movie_service.get_movie(movie_uid, session)
    if movie:
        return movie
    else:
        raise HTTPException(status_code=404, detail=f"电影 ID {movie_uid} 不存在")


@router.post(
    "/",
    response_model=MovieOutput,
    status_code=status.HTTP_201_CREATED,
)
async def create_movie(
    movie_data: MovieCreate,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    user_id = token_details.get("user")["user_uid"]
    new_movie = await movie_service.create_movie(movie_data, user_id, session)
    if not new_movie:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="电影已存在"
        )
    return new_movie


@router.patch("/{movie_uid}", response_model=MovieOutput)
async def update_movie(
    movie_uid: str,
    movie_update: MovieUpdate,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    updated_movie = await movie_service.update_movie(movie_uid, movie_update, session)
    if updated_movie:
        return updated_movie
    else:
        raise HTTPException(status_code=404, detail=f"电影 id{movie_uid}不存在")


@router.delete("/{movie_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    movie_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    deleted_movie = await movie_service.delete_movie(movie_uid, session)
    if deleted_movie:
        return {}
    else:
        raise HTTPException(status_code=404, detail=f"电影 ID {movie_uid} 不存在")
