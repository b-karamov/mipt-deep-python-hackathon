from domain.user import User
from repository.repository import Repository


class UserService:
    def __init__(self, repositories: Repository) -> None:
        self.repositories = repositories

    def create_user(self, username: str) -> User:
        user = User(username)
        return self.repositories.users.save(user)

    def find_by_id(self, id: int) -> User:
        user = self.repositories.users.find_by_id(id)
        if user is None:
            raise LookupError("пользователь не найден")
        return user

    def find_all(self) -> list[User]:
        return self.repositories.users.find_all()
