from app.modules.auth.domain.commands.user_command import RegisterUserCommand
from app.modules.auth.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from app.modules.auth.domain.value_objects.vo import PasswordHashVO, UserCodeVO, EmailVO


class UserCommandHandler:
    
    @staticmethod
    def handle_create_user_command(command: RegisterUserCommand, uok: SqlAlchemyUnitOfWork):
         with uok:
             hash_password = PasswordHashVO.hash_password(command.password)
             email = EmailVO(command.email)
             user_code = UserCodeVO.generate_user_code()
             