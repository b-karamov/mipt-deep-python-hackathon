from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_date: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author: UserResponse
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class CommentReplyCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    author: UserResponse
    parent_id: Optional[int] = None
    created_at: datetime
    replies: List["CommentResponse"] = []
    
    model_config = ConfigDict(from_attributes=True)

# Для рекурсивных ссылок
CommentResponse.model_rebuild()

class CommentTreeResponse(BaseModel):
    comments: List[CommentResponse]
