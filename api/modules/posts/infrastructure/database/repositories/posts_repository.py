from api.modules.posts.domain.repositories.interface_posts_repository import (
    IPostRepository,
)
from modules.posts.domain.entities.post import Post
from modules.posts.infrastructure.database.mappers.posts_mapper import (
    PostsMapper,
)
from modules.posts.infrastructure.database.models.posts import PostSQLAlchemy

from uuid import UUID
from typing import List, Optional


class PostsRepositorySQLAlchemy(IPostRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _save(self, post: Post) -> Post:
        post_orm = PostsMapper.to_orm(post)
        self.session.add(post_orm)
        return post

    def _load(self, post_id: UUID) -> Optional[Post]:
        post_orm = (
            self.session.query(PostSQLAlchemy).filter_by(id=post_id).first()
        )
        if not post_orm:
            return None
        return PostsMapper.to_entity(post_orm)

    # TODO: Implement filters
    def _load_all(self, filters: dict = None) -> List[Post]:
        post_orms = self.session.query(PostSQLAlchemy).all()
        return [PostsMapper.to_entity(post_orm) for post_orm in post_orms]

    def _update(self, post: Post) -> Optional[Post]:
        post_orm = PostsMapper.to_orm(post)
        existing_post_orm = (
            self.session.query(PostSQLAlchemy).filter_by(id=post.id).first()
        )
        if existing_post_orm:
            existing_post_orm.title = post_orm.title
            existing_post_orm.file_url = post_orm.file_url
            existing_post_orm.category = post_orm.category
            existing_post_orm.type = post_orm.type
            existing_post_orm.scores = post_orm.scores
            existing_post_orm.score_avg = post_orm.score_avg
            PostsMapper.base_entity_to_orm(post, existing_post_orm)
            return PostsMapper.to_entity(existing_post_orm)
        else:
            return None

    def _delete(self, post_id: UUID) -> None:
        post_orm = (
            self.session.query(PostSQLAlchemy).filter_by(id=post_id).first()
        )
        if post_orm:
            self.session.delete(post_orm)
