from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from domain.user import User
from repository.tables import users as users_table


class UserRepository:
    """Репозиторий пользователей."""
    def __init__(self, session_factory: async_sessionmaker[AsyncSession] | None = None) -> None:
        self.session_factory = session_factory

    async def save(self, user: User) -> User:
        if self.session_factory is None:
            raise RuntimeError("session_factory не инициализирован")

        async with self.session_factory() as session:
            async with session.begin():
                stmt = insert(users_table).values(
                    username=user.username,
                    created_date=user.created_date,
                )
                result = await session.execute(stmt)
                user_id = result.inserted_primary_key[0]
                user.id = int(user_id)
        return user

    async def find_by_username(self, username: str) -> User | None:
        if self.session_factory is None:
            raise RuntimeError("session_factory не инициализирован")

        async with self.session_factory() as session:
            stmt = select(users_table).where(users_table.c.username == username)
            result = await session.execute(stmt)
            row = result.mappings().one_or_none()
            if row is None:
                return None
            return self._row_to_user(row)

    async def find_by_id(self, id: int) -> User | None:
        if self.session_factory is None:
            raise RuntimeError("session_factory не инициализирован")

        async with self.session_factory() as session:
            stmt = select(users_table).where(users_table.c.id == id)
            result = await session.execute(stmt)
            row = result.mappings().one_or_none()
            if row is None:
                return None
            return self._row_to_user(row)

    async def find_all(self) -> list[User]:
        if self.session_factory is None:
            raise RuntimeError("session_factory не инициализирован")

        async with self.session_factory() as session:
            stmt = select(users_table)
            result = await session.execute(stmt)
            rows = result.mappings().all()
            return [self._row_to_user(r) for r in rows]

    @staticmethod
    def _row_to_user(row) -> User:
        user = User(
            username=row["username"],
            created_date=row["created_date"],
            id=int(row["id"])
        )
        return user
