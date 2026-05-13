from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.db import get_session
from app.schemas.user import UserCreate, UserOutput
from app.service.users_service import user_service

router = APIRouter()


@router.post("/signup", response_model=UserOutput, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exiests = await user_service.user_exiests(email, session)

    if user_exiests:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="用户已经存在"
        )
    new_user = await user_service.create_user(user_data, session)

    return new_user


@router.get("/{email}", response_model=UserOutput)
async def get_user(email: str, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(email, session)

    if user:
        return user
    raise HTTPException(status_code=400, detail="用户不存在")
