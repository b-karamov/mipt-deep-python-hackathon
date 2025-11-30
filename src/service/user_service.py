from domain.user import User
from repository.repository import Repository


class UserService:
    def __init__(self, repositories: Repository) -> None:
        self.repositories = repositories

    async def create_user(self, username: str) -> User:
        user = User(username)
        return await self.repositories.users.save(user)

    async def find_by_id(self, id: int) -> User:
        user = await self.repositories.users.find_by_id(id)
        if user is None:
            raise LookupError("пользователь не найден")
        return user

    async def find_all(self) -> list[User]:
        return await self.repositories.users.find_all()
