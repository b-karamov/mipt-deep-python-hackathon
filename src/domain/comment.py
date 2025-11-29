from __future__ import annotations

from datetime import datetime
from typing import List

from domain.descriptors import AutoIncrementId, NonEmptyString, NonNull
from domain.post import Post
from domain.user import User


class Comment(AutoIncrementId):
    _next_id = 1

    post = NonNull("пост не может быть пустым")
    author = NonNull("автор не может быть пустым")
    text = NonEmptyString("текст комментария не может быть пустым")

    def __init__(
        self,
        post: Post,
        author: User,
        text: str,
        parent: Comment | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.id = self._next()
        self.post = post
        self.author = author
        self.parent = parent
        self.text = text
        self.replies: List[Comment] = []
        self.created_at = created_at or datetime.now()
        if parent is not None:
            parent.add_reply(self)

    @classmethod
    def for_post(cls, post: Post, text: str, author: User) -> Comment:
        if post is None:
            raise ValueError("пост не может быть пустым")
        return cls(post=post, parent=None, text=text, author=author)

    @classmethod
    def reply_to(cls, parent: Comment, text: str, author: User) -> Comment:
        if parent is None:
            raise ValueError("родительский комментарий не может быть пустым")
        return cls(post=parent.post, parent=parent, text=text, author=author)

    def add_reply(self, reply: Comment) -> None:
        if reply is not None:
            self.replies.append(reply)

    def is_reply(self) -> bool:
        return self.parent is not None
