from modules.users.domain.events.admin_events import *
from modules.users.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.users.domain.entities.admin import Admin
from modules.auth.public_api.contracts import AuthPublicAPI
from config.settings import settings, supabase_client

class AdminEventHandler:
    
    @staticmethod
    def handle_admin_updated_event(event: AdminUpdatedEvent, uok: SqlAlchemyUnitOfWork):
        auth_api = AuthPublicAPI()
        auth_api.update_user(
            user_id=event.admin_id,
            email=event.email,
            password=event.password
        )
        
    @staticmethod
    def handle_admin_disabled_event(event: AdminDisabledEvent, uok: SqlAlchemyUnitOfWork):
        auth_api = AuthPublicAPI()
        auth_api.disable_user(
            user_id=event.admin_id
        )
    
    @staticmethod
    def handle_disable_student_account_event(event: DisableStudentAccountEvent, uok: SqlAlchemyUnitOfWork):
        auth_api = AuthPublicAPI()
        auth_api.disable_user(
            user_id=event.student_id
        )