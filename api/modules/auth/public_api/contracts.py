from modules.auth.domain.commands.user_commands import UpdateUserCommand, DisableUserCommand
from modules.auth.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.auth.application.message_bus import MessageBus
from common.session import SessionLocal

class AuthPublicAPI:
    
    def __init__(self):
        self.__uow = SqlAlchemyUnitOfWork(session_factory=SessionLocal)
        self.__message_bus = MessageBus()

    def update_user(self, user_id, email, password):
        print(password)
        command = UpdateUserCommand(user_id=user_id, email=email, password=password)
        return self.__message_bus.handle(command, uok=self.__uow)

    def disable_user(self, user_id):
        command = DisableUserCommand(user_id=user_id)
        return self.__message_bus.handle(command, uok=self.__uow)