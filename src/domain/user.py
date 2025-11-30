from datetime import datetime

from domain.descriptors import NonEmptyString


class User:
    username = NonEmptyString("имя юзера не может быть пустым")

    def __init__(self, username: str, created_date: datetime | None = None, id: int | None = None) -> None:
        self.id = id
        self.username = username
        self.created_date = created_date or datetime.now()
