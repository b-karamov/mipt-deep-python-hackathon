from domain.comment import Comment
from domain.post import Post
from domain.user import User
from repository.repository import Repository


class CommentService:
    def __init__(self, repositories: Repository) -> None:
        self.repositories = repositories

    async def add_comment_to_post(self, post_id: int, username: str, text: str) -> Comment:
        post = await self._require_post(post_id)
        author = await self._require_user(username)
        comment = Comment.for_post(post, text, author)
        return await self.repositories.comments.save(comment)

    async def reply_to_comment(self, comment_id: int, username: str, text: str) -> Comment:
        parent = await self._require_comment(comment_id)
        author = await self._require_user(username)
        reply = Comment.reply_to(parent, text, author)
        return await self.repositories.comments.save(reply)

    async def get_comments_for_post(self, post_id: int) -> list[Comment]:
        post = await self._require_post(post_id)
        return await self.repositories.comments.find_by_post(post.id)

    async def _require_user(self, username: str) -> User:
        user = await self.repositories.users.find_by_username(username)
        if user is None:
            raise LookupError("пользователь не найден")
        return user

    async def _require_post(self, id: int) -> Post:
        post = await self.repositories.posts.find_by_id(id)
        if post is None:
            raise LookupError("пост не найден")
        return post

    async def _require_comment(self, id: int) -> Comment:
        comment = await self.repositories.comments.find_by_id(id)
        if comment is None:
            raise LookupError("комментарий не найден")
        return comment
