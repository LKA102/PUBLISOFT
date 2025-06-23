from modules.auth.domain.commands.user_commands import RegisterUserCommand, LoginUserCommand
from modules.auth.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.auth.domain.value_objects.vo import PasswordHashVO, UserCodeVO, EmailVO
from modules.auth.domain.entities.user import User, UserStateEnum
from modules.auth.domain.services.user_services import validar_credenciales
from config.settings import settings
from jose import jwt 

class UserCommandHandler:
    
    @staticmethod
    def handle_create_user_command(command: RegisterUserCommand, uok: SqlAlchemyUnitOfWork):
         with uok:
            # Create value objects
            email = EmailVO(command.email)
            hash_password = PasswordHashVO.hash_password(command.password)
            user_code = UserCodeVO.generate_user_code()

            # Create the user entity
            user = User.create(
                email=email,
                hash_password=hash_password,
                user_code=user_code,
                name=command.name,
                last_name=command.last_name,
            )

            # Persist the user entity
            uok.user_repository.save(user)
            uok.commit()

    @staticmethod
    def handle_login_user_command(command: LoginUserCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            user = validar_credenciales(
                email=command.email,
                password=command.password,
                uok=uok
            )

            if user.state != UserStateEnum.ACTIVE:
                raise ValueError("User is not active")

            # Maybe should call public API to User module for more data related to student or admin
            user_data_for_token = {
                "id": str(user.id),
                "email": str(user.email),
                "user_code": str(user.user_code),
                "role": user.role,
            }

            # Generate JWT token
            accesstoken = jwt.encode(user_data_for_token, settings.JWT_SECRET)

            # Return the accesstoken
            return accesstoken
             