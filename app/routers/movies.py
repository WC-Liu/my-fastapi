from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.core.dependencies import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
    get_current_user,
)
from app.models.models import Movie
from app.service.movie_service import movie_service

from ..schemas.movie import MovieCreate, MovieOutput, MovieReviewOutPut, MovieUpdate

router = APIRouter()


# 获取所有电影
@router.get(
    "/",
    response_model=List[MovieReviewOutPut],
    dependencies=[Depends(get_current_user)],
)
async def get_movies(session: SessionDep) -> Movie:
    return await movie_service.get_all_movies(session)


# 获取某部电影
@router.get(
    "/{movie_uid}",
    response_model=MovieReviewOutPut,
    dependencies=[Depends(get_current_user)],
)
async def get_movie(movie_uid: str, session: SessionDep) -> Movie:
    return await movie_service.get_movie(movie_uid, session)


# 创建电影
@router.post(
    "/",
    response_model=MovieOutput,
    status_code=status.HTTP_201_CREATED,
)
async def create_movie(
    movie_data: MovieCreate, current_user: CurrentUser, session: SessionDep
) -> Movie:
    user_uid = current_user.uid
    return await movie_service.create_movie(movie_data, user_uid, session)


# 更新电影信息
@router.patch(
    "/{movie_uid}",
    response_model=MovieOutput,
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_movie(
    movie_uid: str, movie_update: MovieUpdate, session: SessionDep
) -> Movie:
    return await movie_service.update_movie(movie_uid, movie_update, session)


# 删除电影
@router.delete(
    "/{movie_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_movie(movie_uid: str, session: SessionDep) -> None:
    await movie_service.delete_movie(movie_uid, session)
