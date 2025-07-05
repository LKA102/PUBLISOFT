from modules.auth.domain.commands.user_commands import RegisterUserCommand, LoginUserCommand, UpdateUserCommand, DisableUserCommand
from modules.auth.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.auth.domain.value_objects.vo import PasswordHashVO, UserCodeVO, EmailVO
from modules.auth.domain.entities.user import User, UserStateEnum, UserRoleEnum
from modules.auth.domain.services.user_services import validar_credenciales
from config.settings import settings
from jose import jwt 

class UserCommandHandler:
    
    @staticmethod
    def handle_create_user_command(command: RegisterUserCommand, uok: SqlAlchemyUnitOfWork):
         with uok:
            # Create value objects
            email = EmailVO(command.email)
            hash_password = PasswordHashVO.generate_hash_password(command.password)
            user_code = UserCodeVO.generate_user_code()
            role = UserRoleEnum.STUDENT if command.role == 0 else UserRoleEnum.ADMIN

            # Create the user entity
            user = User.create(
                email=email,
                hash_password=hash_password,
                user_code=user_code,
                name=command.name,
                last_name=command.last_name,
                role=role
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
             
    @staticmethod
    def handle_update_user_command(command: UpdateUserCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            user = uok.user_repository.load(command.user_id)
            if not user:
                raise ValueError("User not found")

            if command.email:
                print(f"Updating email for user {user.id} to {command.email}")
                user.email = EmailVO(command.email)
            if command.password:
                print(f"Updating password for user {user.id}")
                user.hash_password = PasswordHashVO.generate_hash_password(command.password)

            if command.email or command.password:
                user._update()
            

            uok.user_repository.update(user)
            uok.commit()
            
    @staticmethod
    def handle_disable_user_command(command: DisableUserCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            user = uok.user_repository.load(command.user_id)
            if not user:
                raise ValueError("User not found")

            user.state = UserStateEnum.DELETED
            uok.user_repository.update(user)
            uok.commit()