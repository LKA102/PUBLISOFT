from common.abstract_unit_of_work import AbstractUnitOfWork

from modules.posts.infrastructure.database.repositories.posts_repository import (
    PostsRepositorySQLAlchemy,
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.posts_repository = PostsRepositorySQLAlchemy(session=self.session)

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def collect_events(self):
        for post in self.posts_repository.seen:
            while post.events:
                yield post.events.pop()
