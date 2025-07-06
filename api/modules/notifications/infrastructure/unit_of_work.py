from common.abstract_unit_of_work import AbstractUnitOfWork
from modules.notifications.infrastructure.database.repositories.notification_repository import NotificationRepositorySQLAlchemy

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        # repositories can be initialized here if needed, e.g.:
        self.notification_repository = NotificationRepositorySQLAlchemy(session=self.session)

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        self.session.close()
        
    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
        
    def collect_events(self):
        for notification in self.notification_repository.seen:
            while notification.events:
                yield notification.events.pop()