from fastapi import APIRouter, Depends, status, Query
from typing import List, Annotated

from api.schemas import CommentCreate, CommentReplyCreate, CommentResponse, CommentTreeResponse
from api.dependencies import get_comment_service
from service.comment_service import CommentService


router = APIRouter(prefix="/comments", tags=["comments"])

@router.post(
    "/post/{post_id}",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить комментарий к посту"
)
async def add_comment_to_post(
    post_id: int,
    comment_data: CommentCreate,
    comment_service: Annotated[CommentService, Depends(get_comment_service)],
    username: str = Query(..., description="Имя пользователя, оставляющего комментарий")
):
    """
    Добавить комментарий к посту
    """
    try:
        comment = await comment_service.add_comment_to_post(
            post_id=post_id,
            username=username,
            text=comment_data.text
        )
        return comment
    except (ValueError, LookupError) as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post(
    "/{comment_id}/reply",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ответить на комментарий"
)
async def reply_to_comment(
    comment_id: int,
    reply_data: CommentReplyCreate,
    comment_service: Annotated[CommentService, Depends(get_comment_service)],
    username: str = Query(..., description="Имя пользователя, оставляющего ответ")
):
    """
    Ответить на существующий комментарий
    """
    try:
        reply = await comment_service.reply_to_comment(
            comment_id=comment_id,
            username=username,
            text=reply_data.text
        )
        return reply
    except (ValueError, LookupError) as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/post/{post_id}",
    response_model=List[CommentResponse],
    summary="Получить комментарии к посту"
)
async def get_comments_for_post(
    post_id: int,
    comment_service: Annotated[CommentService, Depends(get_comment_service)]
):
    """Получить все комментарии к посту в виде дерева (с ответами)"""
    try:
        comments = await comment_service.get_comments_for_post(post_id)
        return comments
    except LookupError as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get(
    "/{comment_id}",
    response_model=CommentResponse,
    summary="Получить комментарий по ID"
)
async def get_comment(
    comment_id: int,
    comment_service: Annotated[CommentService, Depends(get_comment_service)]
):
    """Получить информацию о комментарии по ID"""
    comment = await comment_service.repositories.comments.find_by_id(comment_id)
    if not comment:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комментарий не найден"
        )
    return comment
