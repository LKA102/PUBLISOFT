from modules.auth.application.message_bus import MessageBus
from modules.auth.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from common.session import SessionLocal

def get_unit_of_work():
    uok = SqlAlchemyUnitOfWork(session_factory=SessionLocal)
    return uok

def get_message_bus():
    message_bus = MessageBus()
    return message_bus