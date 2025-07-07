from datetime import datetime
from uuid import UUID
from datetime import timezone


class BaseEntity:
    def __init__(self, **kwargs):
        id: int = kwargs.get('id')
        created_at: datetime = kwargs.get('created_at')

        self.__id = id
        self.__created_at = created_at

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def id(self) -> int:
        return self.__id
