from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from domain.comment import Comment
from domain.post import Post
from domain.user import User
from repository.tables import comments as comments_table, posts as posts_table, users as users_table


class CommentRepository:
    """Репозиторий комментариев."""
    def __init__(self, session_factory: async_sessionmaker[AsyncSession] | None = None) -> None:
        self.session_factory = session_factory

    async def save(self, comment: Comment) -> Comment:
        if self.session_factory is None:
            raise RuntimeError("session_factory не инициализирован")

        async with self.session_factory() as session:
            async with session.begin():
                stmt = insert(comments_table).values(
                    post_id=comment.post.id,
                    author_id=comment.author.id,
                    parent_id=comment.parent.id if comment.parent is not None else None,
                    text=comment.text,
                    created_at=comment.created_at,
                )
                result = await session.execute(stmt)
                comment_id = result.inserted_primary_key[0]
                comment.id = int(comment_id)
        return comment

    async def find_by_id(self, id: int) -> Comment | None:
        if self.session_factory is None:
            raise RuntimeError("session_factory не инициализирован")

        async with self.session_factory() as session:
            stmt = select(comments_table).where(comments_table.c.id == id)
            result = await session.execute(stmt)
            row = result.mappings().one_or_none()
            if row is None:
                return None

            post = await self._load_post(session, row["post_id"])
            author = await self._load_user(session, row["author_id"])

            parent = None
            if row["parent_id"] is not None:
                parent = await self._load_comment_simple(session, row["parent_id"], post)

            comment = Comment(
                post=post,
                author=author,
                text=row["text"],
                parent=parent,
                created_at=row["created_at"],
                id=int(row["id"])
            )
            return comment

    async def find_by_post(self, post_id: int) -> list[Comment]:
        """Возвращает дерево комментариев к посту (parent/replies)."""
        if self.session_factory is None:
            raise RuntimeError("session_factory не инициализирован")

        async with self.session_factory() as session:
            post = await self._load_post(session, post_id)

            stmt = (
                select(comments_table)
                .where(comments_table.c.post_id == post_id)
                .order_by(comments_table.c.id)
            )
            result = await session.execute(stmt)
            rows = result.mappings().all()
            if not rows:
                return []

            # Загружаем всех авторов одним запросом
            user_ids = {row["author_id"] for row in rows}
            users_map: dict[int, User] = {}
            if user_ids:
                users_stmt = select(users_table).where(users_table.c.id.in_(user_ids))
                user_rows = (await session.execute(users_stmt)).mappings().all()
                for u_row in user_rows:
                    user = User(
                        username=u_row["username"],
                        created_date=u_row["created_date"],
                        id=int(u_row["id"])
                    )
                    users_map[user.id] = user

            comments_map: dict[int, Comment] = {}
            comments_list: list[Comment] = []

            for row in rows:
                author = users_map[row["author_id"]]
                parent_id = row["parent_id"]
                parent = comments_map.get(parent_id)

                comment = Comment(
                    post=post,
                    author=author,
                    text=row["text"],
                    parent=parent,
                    created_at=row["created_at"],
                    id=int(row["id"])
                )
                comments_map[comment.id] = comment
                comments_list.append(comment)

            return comments_list

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

    @staticmethod
    async def _load_post(session: AsyncSession, post_id: int) -> Post:
        stmt = select(posts_table).where(posts_table.c.id == post_id)
        result = await session.execute(stmt)
        row = result.mappings().one()
        # автор поста
        author_stmt = select(users_table).where(users_table.c.id == row["author_id"])
        author_result = await session.execute(author_stmt)
        author_row = author_result.mappings().one()
        author = User(
            username=author_row["username"],
            created_date=author_row["created_date"],
            id=int(author_row["id"])
        )

        post = Post(
            title=row["title"],
            content=row["content"],
            author=author,
            created_at=row["created_at"],
        )
        post.id = int(row["id"])
        return post

    @staticmethod
    async def _load_comment_simple(
        session: AsyncSession,
        comment_id: int,
        post: Post,
    ) -> Comment:
        """Загрузка родительского комментария без его потомков."""
        stmt = select(comments_table).where(comments_table.c.id == comment_id)
        result = await session.execute(stmt)
        row = result.mappings().one()
        author = await CommentRepository._load_user(session, row["author_id"])
        parent = Comment(
            post=post,
            author=author,
            text=row["text"],
            parent=None,
            created_at=row["created_at"],
            id=int(row["id"])
        )
        return parent
