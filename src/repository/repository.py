from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from repository.comment_repository import CommentRepository
from repository.post_repository import PostRepository
from repository.user_repository import UserRepository


class Repository:
    """Контейнер для всех репозиториев."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory
        self.users = UserRepository(session_factory)
        self.posts = PostRepository(session_factory)
        self.comments = CommentRepository(session_factory)

    def session(self) -> AsyncSession:
        """Создать сессию."""
        return self.session_factory()
