from common.abstract_unit_of_work import AbstractUnitOfWork
from modules.users.infrastructure.database.repositories.student_repository import StudentRepositorySQLAlchemy
from modules.users.infrastructure.database.repositories.admin_repository import AdminRepositorySQLAlchemy

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        # repositories can be initialized here if needed, e.g.:
        self.student_repository = StudentRepositorySQLAlchemy(session=self.session)
        self.admin_repository = AdminRepositorySQLAlchemy(session=self.session)

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        self.session.close()
        
    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
        
    def collect_events(self):
        for student in self.student_repository.seen:
            while student.events:
                yield student.events.pop()
        for admin in self.admin_repository.seen:
            while admin.events:
                yield admin.events.pop()