from datetime import datetime
from uuid import UUID
from datetime import timezone

class BaseEntity:
    def __init__(self, **kwargs):
        id: UUID = kwargs.get('id')
        created_at: datetime = kwargs.get('created_at')
        updated_at: datetime = kwargs.get('updated_at')

        self.__id = id
        self.__created_at = created_at
        self.__updated_at = updated_at

    @property
    def created_at(self) -> datetime:
        return self.__created_at
    
    @property
    def updated_at(self) -> datetime:
        return self.__updated_at
    
    @property
    def id(self) -> UUID:
        return self.__id
    
    def _update(self):
        self.__updated_at = datetime.now(timezone.utc)
