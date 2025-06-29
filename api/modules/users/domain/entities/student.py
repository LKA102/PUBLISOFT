from modules.users.domain.entities.base_entity import BaseEntity
from modules.users.domain.events.student_events import *
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

class Student(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__name: str = kwargs.get('name', "")
        self.__last_name: str = kwargs.get('last_name', "")
        self.__career: str = kwargs.get('career', "")
        self.__faculty: str = kwargs.get('faculty', "")
        self.events = set()

    def __eq__(self, other):
        if not isinstance(other, Student):
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
    def profile_image_path(self) -> str:
        return self.__profile_image_path
    
    @profile_image_path.setter
    def profile_image_path(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Profile image path must be a string")
        self.__profile_image_path = value

    @property
    def career(self) -> str:
        return self.__career
    
    @career.setter
    def career(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Career must be a string")
        self.__career = value

    @property
    def faculty(self) -> str:
        return self.__faculty
    
    @faculty.setter
    def faculty(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Faculty must be a string")
        self.__faculty = value

    # endregion

    @classmethod
    def create(cls, id: UUID, name: str, last_name: str, 
               career: Optional[str] = None, faculty: Optional[str] = None) -> 'Student':
        if not name or not last_name:
            raise ValueError("Name and last name are required")
        
        student = cls(
            id=id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            name=name,
            last_name=last_name,
            career=career,
            faculty=faculty,
        )

        # Return the created Student instance
        return student
    
    def update(self, name: Optional[str] = None, last_name: Optional[str] = None, 
               career: Optional[str] = None, 
               faculty: Optional[str] = None, **extra_data) -> None:
        if name is not None:
            self.name = name
        if last_name is not None:
            self.last_name = last_name
        if career is not None:
            self.career = career
        if faculty is not None:
            self.faculty = faculty
        
        self._update()

        # Emit StudentUpdated event
        student_updated_event = StudentUpdatedEvent(
            student_id=self.id,
            email = extra_data.get('email'),
            password = extra_data.get('password'),
        )

        self.events.add(student_updated_event)

    def disable_account(self) -> None:
        
        # Emit StudentDisabled event
        student_disabled_event = StudentDisabledEvent(
            student_id=self.id
        )
        self.events.add(student_disabled_event)
    
