from modules.users.domain.commands.student_commands import *
from modules.users.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.users.domain.entities.student import Student
from config.settings import settings, supabase_client

class StudentCommandHandler:
    
    @staticmethod
    def handle_create_student_command(command: CreateStudentCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            # Create the student entity
            student = Student.create(
                id=command.id,
                name=command.name,
                last_name=command.last_name
            )
            
            # Persist the student entity
            uok.student_repository.save(student)
            uok.commit()
            
            return student

    @staticmethod
    def handle_update_student_command(command: UpdateStudentCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            student = uok.student_repository.load(command.id)
            if not student:
                raise ValueError("Student not found")
            
            # Update student attributes
            student.update(
                name=command.name,
                last_name=command.last_name,
                email=command.email,
                password=command.password,
                faculty=command.faculty,
                career=command.career
            )
            
            
            # Persist changes
            uok.student_repository.save(student)
            uok.commit()

            return student

    @staticmethod
    def handle_delete_student_command(command: DisableStudentCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            student = uok.student_repository.load(command.id)
            if not student:
                raise ValueError("Student not found")
            
            student.disable_account()
            
            # Delete the student entity
            uok.student_repository.delete(student)
            uok.commit()
            
            return command.id