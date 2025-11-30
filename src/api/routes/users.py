from fastapi import APIRouter, Depends, status
from typing import List, Annotated

from api.schemas import UserCreate, UserResponse
from api.dependencies import get_user_service
from service.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя"
)
async def create_user(
    user_data: UserCreate,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    try:
        user = await user_service.create_user(user_data.username)
        return user
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Получить всех пользователей"
)
async def get_all_users(
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Получить список всех пользователей"""
    return await user_service.find_all()

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Получить пользователя по ID"
)
async def get_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Получить информацию о пользователе по ID"""
    try:
        return await user_service.find_by_id(user_id)
    except LookupError:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
