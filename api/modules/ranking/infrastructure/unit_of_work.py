from common.abstract_unit_of_work import AbstractUnitOfWork
from modules.ranking.infrastructure.database.repositories.ranking_repository import RankingRepositorySQLAlchemy

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        # repositories can be initialized here if needed, e.g.:
        self.ranking_repository = RankingRepositorySQLAlchemy(session=self.session)

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        self.session.close()
        
    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
        
    def collect_events(self):
        for ranking in self.ranking_repository.seen:
            while ranking.events:
                yield ranking.events.pop()