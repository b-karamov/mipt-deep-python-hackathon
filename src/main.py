import shlex
from typing import Dict

from domain.comment import Comment
from domain.post import Post
from domain.user import User
from repository.comment_repository import CommentRepository
from repository.post_repository import PostRepository
from repository.user_repository import UserRepository
from repository.repository import Repository
from service.comment_service import CommentService
from service.post_service import PostService
from service.user_service import UserService


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        super().__init__(session_factory=None)
        self._users: Dict[int, User] = {}

    def save(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def find_by_username(self, username: str) -> User | None:
        return next((u for u in self._users.values() if u.username == username), None)

    def find_by_id(self, id: int) -> User | None:
        return self._users.get(id)

    def find_all(self) -> list[User]:
        return sorted(self._users.values(), key=lambda u: u.id)


class InMemoryPostRepository(PostRepository):
    def __init__(self) -> None:
        super().__init__(session_factory=None)
        self._posts: Dict[int, Post] = {}

    def save(self, post: Post) -> Post:
        self._posts[post.id] = post
        return post

    def find_by_id(self, id: int) -> Post | None:
        return self._posts.get(id)

    def find_by_author(self, author: User) -> list[Post]:
        return self.find_by_author_id(author.id)

    def find_by_author_id(self, author_id: int) -> list[Post]:
        return [p for p in self._posts.values() if p.author.id == author_id]

    def find_all(self) -> list[Post]:
        return sorted(self._posts.values(), key=lambda p: p.id)


class InMemoryCommentRepository(CommentRepository):
    def __init__(self) -> None:
        super().__init__(session_factory=None)
        self._comments: Dict[int, Comment] = {}

    def save(self, comment: Comment) -> Comment:
        self._comments[comment.id] = comment
        return comment

    def find_by_id(self, id: int) -> Comment | None:
        return self._comments.get(id)

    def find_by_post(self, post_id: int) -> list[Comment]:
        return [c for c in self._comments.values() if c.post.id == post_id]


class InMemoryRepository(Repository):
    """Простой контейнер с репозиториями в памяти."""

    def __init__(self) -> None:
        self.users = InMemoryUserRepository()
        self.posts = InMemoryPostRepository()
        self.comments = InMemoryCommentRepository()


def print_help() -> None:
    print(
        "Команды:\n"
        "  user add <username>\n"
        "  user list\n"
        "  post add <username> <title> <content>\n"
        "  post list\n"
        "  comment add <post_id> <username> <text>\n"
        "  comment reply <comment_id> <username> <text>\n"
        "  comment list <post_id>\n"
        "  help\n"
        "  quit\n"
    )


def main() -> None:
    repos = InMemoryRepository()
    user_service = UserService(repos)
    post_service = PostService(repos)
    comment_service = CommentService(repos)

    print("Простой CLI для CommentHub . Используй 'help' для получения подсказки.")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw:
            continue
        parts = shlex.split(raw)
        cmd = parts[0].lower()

        try:
            if cmd == "quit":
                break
            if cmd == "help":
                print_help()
            elif cmd == "user" and len(parts) >= 2:
                sub = parts[1]
                if sub == "add" and len(parts) >= 3:
                    user = user_service.create_user(parts[2])
                    print(f"Создан пользователь: id={user.id}, username={user.username}")
                elif sub == "list":
                    for u in user_service.find_all():
                        print(f"{u.id}: {u.username} (created={u.created_date})")
                else:
                    print("Неправильная user-команда.")
            elif cmd == "post" and len(parts) >= 2:
                sub = parts[1]
                if sub == "add" and len(parts) >= 5:
                    username = parts[2]
                    title = parts[3]
                    content = " ".join(parts[4:])
                    post = post_service.create_post(username, title, content)
                    print(f"Опубликован пост: id={post.id}, title={post.title}, author={post.author.username}")
                elif sub == "list":
                    for p in post_service.repositories.posts.find_all():
                        print(f"{p.id}: {p.title} by {p.author.username}")
                else:
                    print("Неправильная post-команда.")
            elif cmd == "comment" and len(parts) >= 2:
                sub = parts[1]
                if sub == "add" and len(parts) >= 5:
                    post_id = int(parts[2])
                    username = parts[3]
                    text = " ".join(parts[4:])
                    c = comment_service.add_comment_to_post(post_id, username, text)
                    print(f"Создан комментарий: id={c.id} к посту {post_id}")
                elif sub == "reply" and len(parts) >= 5:
                    comment_id = int(parts[2])
                    username = parts[3]
                    text = " ".join(parts[4:])
                    c = comment_service.reply_to_comment(comment_id, username, text)
                    print(f"Создан ответ: id={c.id} к комментарию {comment_id}")
                elif sub == "list" and len(parts) >= 3:
                    post_id = int(parts[2])
                    for c in comment_service.get_comments_for_post(post_id):
                        prefix = f"{c.id} (post {c.post.id})"
                        if c.parent:
                            prefix += f" reply_to={c.parent.id}"
                        print(f"{prefix}: {c.author.username} -> {c.text}")
                else:
                    print("Неправильная comment-команда.")
            else:
                print("Неизвестная команда, попробуй 'help'.")
        except Exception as exc:
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()
