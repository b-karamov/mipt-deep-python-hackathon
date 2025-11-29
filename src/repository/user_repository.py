from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from domain.user import User


class UserRepository:
    """Заглушка."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession] | None = None) -> None:
        self.session_factory = session_factory

    def save(self, user: User) -> User:
        raise NotImplementedError

    def find_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    def find_by_id(self, id: int) -> User | None:
        raise NotImplementedError

    def find_all(self) -> list[User]:
        raise NotImplementedError
