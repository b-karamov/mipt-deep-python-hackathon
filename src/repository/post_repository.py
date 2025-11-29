from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from domain.post import Post
from domain.user import User


class PostRepository:
    """Заглушка."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession] | None = None) -> None:
        self.session_factory = session_factory

    def save(self, post: Post) -> Post:
        raise NotImplementedError

    def find_by_id(self, id: int) -> Post | None:
        raise NotImplementedError

    def find_by_author(self, author: User) -> list[Post]:
        raise NotImplementedError

    def find_by_author_id(self, author_id: int) -> list[Post]:
        raise NotImplementedError

    def find_all(self) -> list[Post]:
        raise NotImplementedError
