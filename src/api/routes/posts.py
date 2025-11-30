from fastapi import APIRouter, Depends, status, Query
from typing import List, Annotated

from api.schemas import PostCreate, PostResponse
from api.dependencies import get_post_service, get_user_service
from service.post_service import PostService
from service.user_service import UserService


router = APIRouter(prefix="/posts", tags=["posts"])

@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пост"
)
async def create_post(
    post_data: PostCreate,
    post_service: Annotated[PostService, Depends(get_post_service)],
    username: str = Query(..., description="Имя пользователя, создающего пост")
):
    try:
        post = await post_service.create_post(
            username=username,
            title=post_data.title,
            content=post_data.content
        )
        return post
    except (ValueError, LookupError) as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=List[PostResponse],
    summary="Получить все посты"
)
async def get_all_posts(
    post_service: Annotated[PostService, Depends(get_post_service)]
):
    """Получить список всех постов"""
    return await post_service.repositories.posts.find_all()

@router.get(
    "/{post_id}",
    response_model=PostResponse,
    summary="Получить пост по ID"
)
async def get_post(
    post_id: int,
    post_service: Annotated[PostService, Depends(get_post_service)]
):
    """Получить информацию о посте по ID"""
    post = await post_service.repositories.posts.find_by_id(post_id)
    if not post:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    return post

@router.get(
    "/author/{username}",
    response_model=List[PostResponse],
    summary="Получить посты пользователя"
)
async def get_posts_by_author(
    username: str,
    post_service: Annotated[PostService, Depends(get_post_service)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Получить все посты конкретного пользователя"""
    user = await user_service.repositories.users.find_by_username(username)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return await post_service.repositories.posts.find_by_author(user)
