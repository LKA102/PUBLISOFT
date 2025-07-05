from modules.auth.domain.events.user_events import *
from modules.auth.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.auth.domain.entities.user import User, UserRoleEnum

from config.settings import settings

class UserEventHandler:
    
    @staticmethod
    def handle_user_created_event(event: UserCreatedEvent, uok: SqlAlchemyUnitOfWork):
        from modules.users.public_api.contracts import UsersPublicAPI
        users_api = UsersPublicAPI()
        if event.role == UserRoleEnum.ADMIN:
            users_api.create_admin(
                id=event.user_id,
                name=event.name,
                last_name=event.last_name
            )
        else:
            users_api.create_student(
                id=event.user_id,
                name=event.name,
                last_name=event.last_name
            )