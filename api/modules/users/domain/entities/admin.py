from modules.users.domain.entities.base_entity import BaseEntity
from modules.users.domain.events.admin_events import *
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

class Admin(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__name: str = kwargs.get('name', "")
        self.__last_name: str = kwargs.get('last_name', "")
        self.__faculty: str = kwargs.get('faculty', "")
        self.events = set()


    
