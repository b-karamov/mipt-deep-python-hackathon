from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi import Depends, HTTPException, status
from typing import Annotated, AsyncGenerator

from config import settings
from repository.repository import Repository
from service.user_service import UserService
from service.post_service import PostService
from service.comment_service import CommentService


# Настройка базы данных
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[Repository, None]:
    async with async_session_factory() as session:
        repos = Repository(session_factory=async_session_factory)
        try:
            yield repos
        finally:
            pass

async def get_user_service(
    repos: Annotated[Repository, Depends(get_db)]
) -> UserService:
    return UserService(repos)

async def get_post_service(
    repos: Annotated[Repository, Depends(get_db)]
) -> PostService:
    return PostService(repos)

async def get_comment_service(
    repos: Annotated[Repository, Depends(get_db)]
) -> CommentService:
    return CommentService(repos)


# Общие зависимости для проверки существования сущностей
async def require_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    try:
        return await user_service.find_by_id(user_id)
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

async def require_post(
    post_id: int,
    post_service: Annotated[PostService, Depends(get_post_service)]
):
    try:
        return await post_service.repositories.posts.find_by_id(post_id)
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
