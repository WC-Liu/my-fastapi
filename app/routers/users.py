from uuid import UUID

from typing import List

from fastapi import APIRouter, Depends, status

from app.core.dependencies import SessionDep, get_current_active_superuser
from app.models.models import User
from app.schemas.auth import ApiResponse, UserOutput, UserUpdate
from app.service.user_service import user_service

router = APIRouter()


@router.get(
    "/",
    response_model=ApiResponse[List[UserOutput]],
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_all_users(session: SessionDep) -> ApiResponse[List[User]]:
    users = await user_service.get_all_users(session)
    return ApiResponse(data=users)


@router.get(
    "/{user_uid}",
    response_model=ApiResponse[UserOutput],
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_user(user_uid: UUID, session: SessionDep) -> ApiResponse[User]:
    user = await user_service.get_user_by_user_uid(user_uid, session)
    return ApiResponse(data=user)


@router.patch(
    "/{user_uid}",
    response_model=ApiResponse[UserOutput],
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_user(
    user_uid: UUID, user_update: UserUpdate, session: SessionDep
) -> ApiResponse[User]:
    updated_user = await user_service.update_user(user_uid, user_update, session)
    return ApiResponse(data=updated_user)


@router.delete(
    "/{user_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_user(user_uid: UUID, session: SessionDep) -> None:
    await user_service.delete_user(user_uid, session)
