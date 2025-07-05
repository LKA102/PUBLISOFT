from datetime import datetime
from uuid import UUID
from datetime import timezone


class BaseEntity:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    def _update(self):
        self.__updated_at = datetime.now(timezone.utc)
