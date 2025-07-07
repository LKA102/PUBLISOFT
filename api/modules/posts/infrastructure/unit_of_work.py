from common.abstract_unit_of_work import AbstractUnitOfWork

from modules.posts.infrastructure.database.repositories.posts_repository import (
    PostsRepositorySQLAlchemy,
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = None
        self._posts_repository = None

    def __enter__(self):
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        if self.session:
            self.session.close()

    @property
    def posts_repository(self):
        if self._posts_repository is None:
            if self.session is None:
                self.session = self.session_factory()
            self._posts_repository = PostsRepositorySQLAlchemy(
                session=self.session
            )
        return self._posts_repository

    def commit(self):
        if self.session:
            self.session.commit()

    def rollback(self):
        if self.session:
            self.session.rollback()

    def collect_events(self):
        if self._posts_repository:
            for post in self._posts_repository.seen:
                while post.events:
                    yield post.events.pop()
