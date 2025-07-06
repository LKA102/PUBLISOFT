from datetime import datetime
from uuid import UUID
from datetime import timezone


class BaseEntity:
    def __init__(self, **kwargs):
        id: int = kwargs.get('id')
        fecha_creacion: datetime = kwargs.get('fecha_creacion')

        self.__id = id
        self.__fecha_creacion = fecha_creacion

    @property
    def fecha_creacion(self) -> datetime:
        return self.__fecha_creacion
    
    @property
    def id(self) -> int:
        return self.__id
