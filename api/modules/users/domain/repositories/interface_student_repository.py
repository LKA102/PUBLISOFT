from abc import ABC, abstractmethod
from modules.users.domain.entities.student import Student
from typing import Set
from uuid import UUID

class IStudentRepository(ABC):
    def __init__(self):
        self.seen: Set[Student] = set()

    @abstractmethod
    def _load(self, student_id: UUID) -> Student:
        """
        Load a student by their ID.
        """
        pass

    @abstractmethod
    def _load_all(self) -> Set[Student]:
        """
        Load all students.
        """
        pass

    @abstractmethod
    def _save(self, student: Student) -> Student:
        """
        Save a student to the repository.
        """
        pass

    @abstractmethod
    def _update(self, student: Student) -> Student:
        """
        Update an existing student in the repository.
        """
        pass

    def load(self, student_id: UUID) -> Student:
        """
        Load a student by their ID, using the internal _load method.
        """
        student = self._load(student_id)
        self.seen.add(student)
        return student
    
    def load_all(self) -> Set[Student]:
        """
        Load all students, using the internal _load_all method.
        """
        students = self._load_all()
        self.seen.update(students)
        return students
    
    def save(self, student: Student) -> Student:
        """
        Save a student to the repository, using the internal _save method.
        """
        saved_student = self._save(student)
        self.seen.add(saved_student)
        return saved_student
    
    def update(self, student: Student) -> Student:
        """
        Update a student in the repository, using the internal _update method.
        """
        updated_student = self._update(student)
        self.seen.add(updated_student)
        return updated_student