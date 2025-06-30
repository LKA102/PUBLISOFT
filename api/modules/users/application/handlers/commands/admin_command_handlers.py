from api.modules.users.domain.entities import admin
from modules.users.domain.commands.admin_commands import *
from modules.users.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.users.domain.entities.admin import Admin
from config.settings import settings, supabase_client

class AdminCommandHandler:

    @staticmethod
    def handle_create_admin_command(command: CreateAdminCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            admin = Admin.create(
                id=command.id,
                name=command.name,
                last_name=command.last_name,
            )
            uok.admin_repository.save(admin)
            uok.commit()
            return admin

    @staticmethod
    def handle_update_admin_command(command: UpdateAdminCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            admin = uok.admin_repository.load(command.id)
            if not admin:
                raise ValueError("Admin not found")

            admin.update(
                name=command.name,
                last_name=command.last_name,
                faculty=command.faculty,
                email=command.email,
                password=command.password
            )

            uok.admin_repository.save(admin)
            uok.commit()
            return admin

    @staticmethod
    def handle_delete_admin_command(command: DisableAdminCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            admin = uok.admin_repository.load(command.id)
            if not admin:
                raise ValueError("Admin not found")

            admin.disable_account()
            uok.commit()
            return admin

    @staticmethod
    def handle_disable_student_account_command(command: DisableStudentAccountCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            student = uok.student_repository.load(command.student_id)
            if not student:
                raise ValueError("Student not found")

            admin.disable_student_account(command.student_id)
            uok.commit()
            return student.id
