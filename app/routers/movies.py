from typing import List

from fastapi import APIRouter, Depends, status

from app.core.dependencies import (
    SessionDep,
    get_current_active_superuser,
    get_current_user,
)
from app.service.movie_service import movie_service

from ..schemas.auth import ApiResponse
from ..schemas.movie import MovieCreate, MovieOutput, MovieReviewOutPut, MovieUpdate

router = APIRouter()


@router.get(
    "",
    response_model=ApiResponse[List[MovieReviewOutPut]],
    dependencies=[Depends(get_current_user)],
)
async def get_movies(session: SessionDep) -> ApiResponse[List[MovieReviewOutPut]]:
    movies = await movie_service.get_all_movies(session)
    return ApiResponse(data=movies)


@router.get(
    "/{movie_uid}",
    response_model=ApiResponse[MovieReviewOutPut],
    dependencies=[Depends(get_current_user)],
)
async def get_movie(
    movie_uid: str, session: SessionDep
) -> ApiResponse[MovieReviewOutPut]:
    movie = await movie_service.get_movie(movie_uid, session)
    return ApiResponse(data=movie)


@router.post(
    "",
    response_model=ApiResponse[MovieOutput],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_movie(
    movie_data: MovieCreate, session: SessionDep
) -> ApiResponse[MovieOutput]:
    movie = await movie_service.create_movie(movie_data, session)
    return ApiResponse(data=movie)


@router.patch(
    "/{movie_uid}",
    response_model=ApiResponse[MovieOutput],
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_movie(
    movie_uid: str, movie_update: MovieUpdate, session: SessionDep
) -> ApiResponse[MovieOutput]:
    movie = await movie_service.update_movie(movie_uid, movie_update, session)
    return ApiResponse(data=movie)


@router.delete(
    "/{movie_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_movie(movie_uid: str, session: SessionDep) -> None:
    await movie_service.delete_movie(movie_uid, session)
