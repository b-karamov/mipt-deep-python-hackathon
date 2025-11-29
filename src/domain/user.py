from datetime import datetime

from domain.descriptors import AutoIncrementId, NonEmptyString


class User(AutoIncrementId):
    _next_id = 1

    username = NonEmptyString("имя юзера не может быть пустым")

    def __init__(self, username: str, created_date: datetime | None = None) -> None:
        self.id = self._next()
        self.username = username
        self.created_date = created_date or datetime.now()
