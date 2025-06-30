from modules.users.domain.entities.base_entity import BaseEntity
from modules.users.domain.events.admin_events import *
from modules.users.domain.services.services import *
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

class Admin(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__name: str = kwargs.get('name', "")
        self.__last_name: str = kwargs.get('last_name', "")
        self.__faculty: Optional[str] = kwargs.get('faculty', None)
        self.events = set()
        
    def __eq__(self, other):
        if not isinstance(other, Admin):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
    # region GETTERS AND SETTERS
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self.__name = value
    
    @property
    def last_name(self) -> str:
        return self.__last_name
    
    @last_name.setter
    def last_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Last name must be a string")
        self.__last_name = value
        
    @property
    def faculty(self) -> str:
        return self.__faculty
    
    @faculty.setter
    def faculty(self, value: Optional[str] = None):
        if not isinstance(value, str) and value is not None:
            raise ValueError("Faculty must be a string")
        self.__faculty = value
    
    # endregion

    @classmethod
    def create(cls, name: str, last_name: str, faculty: Optional[str] = None, id: Optional[UUID] = None) -> 'Admin':
        if not name or not last_name:
            raise ValueError("Name and last name are required")

        if id is None:
            id = uuid4()

        admin = cls(
            id=id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            name=name,
            last_name=last_name,
            faculty=faculty
        )

        # Return the created Admin instance
        return admin

    def update(self, name: Optional[str] = None, last_name: Optional[str] = None, 
               faculty: Optional[str] = None, **extra_data) -> None:
        if name is not None:
            self.name = name
        if last_name is not None:
            self.last_name = last_name
        if faculty is not None:
            self.faculty = faculty
        
        self._update()
        
        email = extra_data.get('email')
        password = extra_data.get('password')
        
        if email is not None or password is not None:
            
            if email is not None:
                if not validate_email_format(email):
                    raise ValueError("Invalid email format")

            # Emit AdminUpdatedEvent
            admin_updated_event = AdminUpdatedEvent(
                admin_id=self.id,
                email=email,
                password=password
            )

            self.events.add(admin_updated_event)
        
    def disable_account(self) -> None:
        
        # Emit AdminDisabled event
        admin_disabled_event = AdminDisabledEvent(
            id=self.id
        )
        self.events.add(admin_disabled_event)

    def disable_student_account(self, student_id: UUID) -> None:

        # Emit DisableStudentAccountEvent
        disable_student_event = DisableStudentAccountEvent(student_id=student_id)
        self.events.add(disable_student_event)