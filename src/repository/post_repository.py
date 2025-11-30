from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from domain.post import Post
from domain.user import User
from repository.tables import posts as posts_table, users as users_table


class PostRepository:
    """Репозиторий постов."""
    def __init__(self, session_factory: async_sessionmaker[AsyncSession] | None = None) -> None:
        self.session_factory = session_factory

    async def save(self, post: Post) -> Post:
        if self.session_factory is None:
            raise RuntimeError("session_factory не инициализирован")

        async with self.session_factory() as session:
            async with session.begin():
                stmt = insert(posts_table).values(
                    title=post.title,
                    content=post.content,
                    author_id=post.author.id,
                    created_at=post.created_at,
                )
                result = await session.execute(stmt)
                post_id = result.inserted_primary_key[0]
                post.id = int(post_id)
        return post

    async def find_by_id(self, id: int) -> Post | None:
        if self.session_factory is None:
            raise RuntimeError("session_factory не инициализирован")

        async with self.session_factory() as session:
            stmt = select(posts_table).where(posts_table.c.id == id)
            result = await session.execute(stmt)
            row = result.mappings().one_or_none()
            if row is None:
                return None

            author = await self._load_user(session, row["author_id"])
            post = Post(
                title=row["title"],
                content=row["content"],
                author=author,
                created_at=row["created_at"],
                id=int(row["id"])
            )
            return post

    async def find_by_author(self, author: User) -> list[Post]:
        return await self.find_by_author_id(author.id)

    async def find_by_author_id(self, author_id: int) -> list[Post]:
        if self.session_factory is None:
            raise RuntimeError("session_factory не инициализирован")

        async with self.session_factory() as session:
            stmt = select(posts_table).where(posts_table.c.author_id == author_id)
            result = await session.execute(stmt)
            rows = result.mappings().all()
            if not rows:
                return []

            author = await self._load_user(session, author_id)
            posts: list[Post] = []
            for row in rows:
                post = Post(
                    title=row["title"],
                    content=row["content"],
                    author=author,
                    created_at=row["created_at"],
                    id=int(row["id"])
                )
                posts.append(post)
            return posts

    async def find_all(self) -> list[Post]:
        if self.session_factory is None:
            raise RuntimeError("session_factory не инициализирован")

        async with self.session_factory() as session:
            stmt = select(posts_table)
            result = await session.execute(stmt)
            rows = result.mappings().all()
            if not rows:
                return []

            author_ids = {row["author_id"] for row in rows}
            authors: dict[int, User] = {}
            for aid in author_ids:
                authors[aid] = await self._load_user(session, aid)

            posts: list[Post] = []
            for row in rows:
                author = authors[row["author_id"]]
                post = Post(
                    title=row["title"],
                    content=row["content"],
                    author=author,
                    created_at=row["created_at"],
                    id=int(row["id"])
                )
                posts.append(post)
            return posts

    @staticmethod
    async def _load_user(session: AsyncSession, user_id: int) -> User:
        stmt = select(users_table).where(users_table.c.id == user_id)
        result = await session.execute(stmt)
        row = result.mappings().one()
        user = User(
            username=row["username"],
            created_date=row["created_date"],
            id=int(row["id"])
        )
        return user
