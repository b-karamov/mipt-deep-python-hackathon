from domain.comment import Comment
from domain.post import Post
from domain.user import User
from repository.repository import Repository


class CommentService:
    def __init__(self, repositories: Repository) -> None:
        self.repositories = repositories

    def add_comment_to_post(self, post_id: int, username: str, text: str) -> Comment:
        post = self._require_post(post_id)
        author = self._require_user(username)
        comment = Comment.for_post(post, text, author)
        return self.repositories.comments.save(comment)

    def reply_to_comment(self, comment_id: int, username: str, text: str) -> Comment:
        parent = self._require_comment(comment_id)
        author = self._require_user(username)
        reply = Comment.reply_to(parent, text, author)
        return self.repositories.comments.save(reply)

    def get_comments_for_post(self, post_id: int) -> list[Comment]:
        post = self._require_post(post_id)
        return self.repositories.comments.find_by_post(post.id)

    def _require_user(self, username: str) -> User:
        user = self.repositories.users.find_by_username(username)
        if user is None:
            raise LookupError("пользователь не найден")
        return user

    def _require_post(self, id: int) -> Post:
        post = self.repositories.posts.find_by_id(id)
        if post is None:
            raise LookupError("пост не найден")
        return post

    def _require_comment(self, id: int) -> Comment:
        comment = self.repositories.comments.find_by_id(id)
        if comment is None:
            raise LookupError("комментарий не найден")
        return comment
