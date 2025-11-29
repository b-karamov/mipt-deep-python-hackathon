from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from domain.comment import Comment


class CommentRepository:
    """Заглушка."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession] | None = None) -> None:
        self.session_factory = session_factory

    def save(self, comment: Comment) -> Comment:
        raise NotImplementedError

    def find_by_id(self, id: int) -> Comment | None:
        raise NotImplementedError

    def find_by_post(self, post_id: int) -> list[Comment]:
        raise NotImplementedError
