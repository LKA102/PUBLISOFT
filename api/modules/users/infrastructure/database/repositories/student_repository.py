from typing import Set, Optional
from modules.users.domain.entities.student import Student
from modules.users.domain.repositories.interface_student_repository import IStudentRepository
from modules.users.infrastructure.database.models.students import StudentSQLAlchemy
from modules.users.infrastructure.database.mappers.student_mapper import StudentMapper
from uuid import UUID

class StudentRepositorySQLAlchemy(IStudentRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _save(self, student: Student) -> Student:
        student_orm = StudentMapper.to_orm(student, self.session)
        self.session.add(student_orm)
        return student

    def _load(self, student_id: UUID) -> Optional[Student]:
        student_orm = self.session.query(StudentSQLAlchemy).filter_by(id=student_id).first()
        if not student_orm:
            return None
        return StudentMapper.to_entity(student_orm)

    def _load_all(self) -> Set[Student]:
        students_orm = self.session.query(StudentSQLAlchemy).all()
        return {StudentMapper.to_entity(student_orm) for student_orm in students_orm}

    def _update(self, student: Student) -> Optional[Student]:
        student_orm = StudentMapper.to_orm(student, self.session)
        existing_student_orm = self.session.query(StudentSQLAlchemy).filter_by(id=student.id).first()
        if existing_student_orm:
            existing_student_orm.name = student_orm.name
            existing_student_orm.email = student_orm.email
            existing_student_orm.state = student_orm.state
            existing_student_orm.student_code = student_orm.student_code
            StudentSQLAlchemy.base_entity_to_orm(student, existing_student_orm)
            return StudentMapper.to_entity(existing_student_orm)
        else:
            return None