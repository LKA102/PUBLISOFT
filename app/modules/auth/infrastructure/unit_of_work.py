from app.common.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.auth.infrastructure.database.repositories.user_repository import UserRepositorySQLAlchemy

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        # repositories can be initialized here if needed, e.g.:
        self.user_repository = UserRepositorySQLAlchemy(session=self.session)

    def __exit__(self, *args):
        super().__exit__(args)
        self.session.close()
        
    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
        
    def collect_events(self):
        for user in self.user_repository.seen:
            while user.events:
                yield user.events.pop()