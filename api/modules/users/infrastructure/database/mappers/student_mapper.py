from modules.users.domain.entities.student import Student
from modules.users.infrastructure.database.models.students import StudentSQLAlchemy
from modules.users.infrastructure.database.models.base_entity import BaseEntitySQLAlchemy

class StudentMapper:
    @staticmethod
    def to_entity(student_orm: StudentSQLAlchemy) -> Student:
        # Convert ORM model to domain entity
        base_kwargs = BaseEntitySQLAlchemy.orm_to_base_entity(student_orm)
        return Student(
            name=student_orm.name,
            last_name=student_orm.last_name,
            career=student_orm.career,
            faculty=student_orm.faculty,
            profile_image_path=student_orm.profile_image_path,
            **base_kwargs
        )

    @staticmethod
    def to_orm(student: Student, **kwargs) -> StudentSQLAlchemy:
        student_orm = StudentSQLAlchemy()
        student_orm.name = student.name
        student_orm.last_name = student.last_name
        student_orm.career = student.career
        student_orm.faculty = student.faculty
        student_orm.profile_image_path = kwargs.get('profile_image_path', None)
        StudentSQLAlchemy.base_entity_to_orm(student, student_orm)
        return student_orm