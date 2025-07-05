from modules.users.domain.events.student_events import *
from modules.users.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.users.domain.entities.student import Student
from config.settings import settings, supabase_client

class StudentEventHandler:
    
    @staticmethod
    def handle_student_updated_event(event: StudentUpdatedEvent, uok: SqlAlchemyUnitOfWork):
        from modules.auth.public_api.contracts import AuthPublicAPI
        auth_api = AuthPublicAPI()
        auth_api.update_user(
            user_id=event.student_id,
            email=event.email,
            password=event.password
        )
        
    @staticmethod
    def handle_student_disabled_event(event: StudentDisabledEvent, uok: SqlAlchemyUnitOfWork):
        from modules.auth.public_api.contracts import AuthPublicAPI
        auth_api = AuthPublicAPI()
        auth_api.disable_user(
            user_id=event.student_id
        )