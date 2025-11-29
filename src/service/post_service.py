from domain.post import Post
from repository.repository import Repository


class PostService:
    def __init__(self, repositories: Repository) -> None:
        self.repositories = repositories

    def create_post(self, username: str, title: str, content: str) -> Post:
        author = self.repositories.users.find_by_username(username)
        if author is None:
            raise LookupError("пользователь не найден")
        post = Post(title, content, author)
        return self.repositories.posts.save(post)
