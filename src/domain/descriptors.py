class NonEmptyString:
    """Дескриптор для непустых строковых полей."""

    def __init__(self, message: str) -> None:
        self.message = message
        self.private_name: str | None = None

    def __set_name__(self, owner, name) -> None:
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance, value) -> None:
        if not isinstance(value, str) or not value:
            raise ValueError(self.message)
        setattr(instance, self.private_name, value)


class NonNull:
    """Дескриптор для полей, которые не могут быть пустыми."""

    def __init__(self, message: str) -> None:
        self.message = message
        self.private_name: str | None = None

    def __set_name__(self, owner, name) -> None:
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance, value) -> None:
        if value is None:
            raise ValueError(self.message)
        setattr(instance, self.private_name, value)


class _IdProtectedMeta(type):
    """Метакласс для блокировки изменения _next_id извне."""

    def __setattr__(cls, name, value):
        if name == "_next_id":
            raise AttributeError("Прямые изменения _next_id запрещены")
        super().__setattr__(name, value)


class AutoIncrementId(metaclass=_IdProtectedMeta):
    """Базовый класс для классов с полем _next_id."""

    _next_id = 1

    @classmethod
    def _next(cls) -> int:
        current = cls._next_id
        type.__setattr__(cls, "_next_id", current + 1)
        return current
