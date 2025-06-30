from modules.users.domain.commands.admin_commands import CreateAdminCommand
from modules.users.domain.commands.student_commands import CreateStudentCommand
from modules.users.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.users.application.message_bus import MessageBus
from common.session import SessionLocal

class UsersPublicAPI:
    def __init__(self):
        self.__uow = SqlAlchemyUnitOfWork(session_factory=SessionLocal)
        self.__message_bus = MessageBus()

    def create_admin(self, name, last_name, email, password):
        command = CreateAdminCommand(name=name, last_name=last_name, email=email, password=password)
        return self.__message_bus.handle(command, uok=self.__uow)

    def create_student(self, name, last_name, email, password):
        command = CreateStudentCommand(name=name, last_name=last_name, email=email, password=password)
        return self.__message_bus.handle(command, uok=self.__uow)