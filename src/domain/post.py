from datetime import datetime

from domain.descriptors import AutoIncrementId, NonEmptyString, NonNull
from domain.user import User


class Post(AutoIncrementId):
    _next_id = 1

    title = NonEmptyString("заголовок поста не может быть пустым")
    content = NonEmptyString("пост не может быть пустым")
    author = NonNull("автор не может быть пустым")

    def __init__(
        self,
        title: str,
        content: str,
        author: User,
        created_at: datetime | None = None,
    ) -> None:
        self.id = self._next()
        self.title = title
        self.content = content
        self.author = author
        self.created_at = created_at or datetime.now()
