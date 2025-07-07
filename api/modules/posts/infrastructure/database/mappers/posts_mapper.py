from modules.posts.domain.entities.post import Post, PostTypeEnum
from modules.posts.infrastructure.database.models.posts import PostSQLAlchemy
from modules.posts.infrastructure.database.models.base_entity import (
    BaseEntitySQLAlchemy,
)
from modules.posts.domain.value_objects.vo import CategoryVO, ScoreVO
from uuid import UUID


class PostsMapper:
    @staticmethod
    def to_entity(post_orm: PostSQLAlchemy) -> Post:
        base_kwargs = BaseEntitySQLAlchemy.orm_to_base_entity(post_orm)

        category = CategoryVO(post_orm.category)
        type = PostTypeEnum(post_orm.type)

        scores = []
        for score_data in post_orm.scores:
            if (
                isinstance(score_data, dict)
                and "student_id" in score_data
                and "score" in score_data
            ):
                scores.append(
                    ScoreVO(
                        student_id=UUID(score_data["student_id"]),
                        score=score_data["score"],
                    )
                )
            elif isinstance(score_data, int):
                # Handle legacy/broken data that only has score values
                continue

        return Post(
            title=post_orm.title,
            file_url=post_orm.file_url,
            original_filename=post_orm.original_filename,
            category=category,
            type=type,
            scores=scores,
            score_avg=post_orm.score_avg,
            author_id=post_orm.author_id,
            **base_kwargs,
        )

    @staticmethod
    def to_orm(post: Post) -> PostSQLAlchemy:
        scores = []
        for score in post.scores:
            scores.append(
                {"student_id": str(score.student_id), "score": score.score}
            )

        post_orm = PostSQLAlchemy()
        post_orm.title = post.title
        post_orm.file_url = post.file_url
        post_orm.original_filename = post.original_filename
        post_orm.category = post.category.name
        post_orm.type = post.type.value
        post_orm.scores = scores
        post_orm.score_avg = post.score_avg
        post_orm.author_id = post.author_id

        # Only set ID if it's not the placeholder UUID
        if post.id and post.id != UUID(int=0):
            post_orm.id = post.id
        post_orm.created_at = post.created_at
        post_orm.updated_at = post.updated_at

        return post_orm
