from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.dependencies import get_current_active_superuser
from app.db.db import get_session
from app.models.models import User
from app.schemas.auth import UserMoviesOutput, UserOutput, UserUpdate
from app.service.user_service import user_service

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserOutput],
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_all_users(
    session: AsyncSession = Depends(get_session),
):
    users = await user_service.get_all_users(session)
    if not users:
        raise HTTPException(status_code=403, detail="查询失败")
    return users


@router.get("/{user_uid}", response_model=UserOutput)
async def get_user(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
):
    user = await user_service.get_user_by_user_uid(user_uid, session)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.patch("/{user_uid}", response_model=UserOutput)
async def update_user(
    user_uid: str,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_session),
):
    updated_user = await user_service.update_user(user_uid, user_update, session)
    if not updated_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return updated_user


@router.delete("/{user_uid}")
async def delete_user(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
):
    result = await user_service.delete_user(user_uid, session)
    if not result:
        raise HTTPException(status_code=400, detail="用户不存在")
    return {}


@router.get(
    "/{user_uid}/movies",
    response_model=List[UserMoviesOutput],
)
async def get_user_movie_sub(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
):
    movies = await user_service.get_user_movies(user_uid, session)
    return movies
