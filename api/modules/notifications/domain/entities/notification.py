from modules.notifications.domain.entities.base_entity import BaseEntity
# from modules.notifications.domain.events.user_events import UserCreatedEvent
from typing import List, Optional
import enum
import uuid
from datetime import datetime, timezone

class NotificationTypeEnum(str, enum.Enum):
    CONNECTION = "CONNECTION"
    APPRECIATION = "APPRECIATION"
    REACTION = "REACTION"

class Notification(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__title: str = kwargs.get('title', "")
        self.__message: str = kwargs.get('message', "")
        self.__type: NotificationTypeEnum = kwargs.get('type')
        self.__user_emisor_id: uuid.UUID = kwargs.get('user_emisor_id')
        self.__user_receptor_id: uuid.UUID = kwargs.get('user_receptor_id')
        self.events: set = set()

    def __eq__(self, other):
        if not isinstance(other, Notification):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

    # region GETTERS AND SETTERS

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str):
        if not value:
            raise ValueError("El título no puede estar vacío")
        self.__title = value

    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, value: str):
        if not value:
            raise ValueError("El mensaje no puede estar vacío")
        self.__message = value

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value

    @property
    def leido(self) -> bool:
        return self.__leido

    @leido.setter
    def leido(self, value: bool):
        self.__leido = value

    @property
    def user_emisor_id(self) -> str:
        return self.__user_emisor_id

    @property
    def user_receptor_id(self) -> str:
        return self.__user_receptor_id


    @classmethod
    def create(cls, id: int, title: str, message: str, type: str, user_emisor_id: uuid.UUID, user_receptor_id: uuid.UUID,
               leido: bool, fecha_creacion: datetime) -> 'Notification':

        notification = cls(
            id=id,
            title=title,
            message=message,
            type=type,
            leido=leido,
            user_emisor_id=user_emisor_id,
            user_receptor_id=user_receptor_id,
            fecha_creacion=fecha_creacion
        )
        return notification