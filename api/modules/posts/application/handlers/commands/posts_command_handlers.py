from modules.posts.domain.entities.post import Post, PostTypeEnum
from modules.posts.domain.value_objects.vo import CategoryVO
from modules.posts.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.posts.domain.commands.post_commands import CreatePostCommand
from modules.posts.domain.commands.post_commands import UpdatePostCommand
from modules.posts.domain.commands.post_commands import DeletePostCommand
from modules.posts.domain.commands.post_commands import ScorePostCommand
from config.settings import supabase_client


class PostsCommandHandler:
    @staticmethod
    def handle_create_post_command(
        command: CreatePostCommand, uok: SqlAlchemyUnitOfWork
    ) -> Post:
        with uok:
            category = CategoryVO(command.category)
            post_type = PostTypeEnum(command.type)

            file_url = supabase_client.storage.from_("posts").upload(
                path=command.file.filename,
                file=command.file,
                file_options={
                    "upsert": True,
                },
            )

            post = Post.create(
                title=command.title,
                file_url=file_url,
                category=category,
                type=post_type,
            )

            saved_post = uok.post_repository.save(post)
            uok.commit()

            return saved_post

    @staticmethod
    def handle_update_post_command(
        command: UpdatePostCommand, uok: SqlAlchemyUnitOfWork
    ) -> Post:
        with uok:
            post = uok.post_repository.load(command.post_id)
            if not post:
                raise ValueError("Post not found")

            if command.category:
                category = CategoryVO(command.category)
            if command.type:
                post_type = PostTypeEnum(command.type)

            if command.title:
                post.title = command.title
            if command.file_url:
                post.file_url = command.file_url
            if command.category:
                post.category = category
            if command.type:
                post.type = post_type

            updated_post = uok.post_repository.update(post)
            uok.commit()

            return updated_post

    @staticmethod
    def handle_delete_post_command(
        command: DeletePostCommand, uok: SqlAlchemyUnitOfWork
    ):
        with uok:
            post = uok.post_repository.load(command.post_id)
            if not post:
                raise ValueError("Post not found")

            uok.post_repository.delete(command.post_id)
            uok.commit()

    @staticmethod
    def handle_score_post_command(
        command: ScorePostCommand, uok: SqlAlchemyUnitOfWork
    ):
        with uok:
            post = uok.post_repository.load(command.post_id)
            if not post:
                raise ValueError("Post not found")

            post.score_post(command.student_id, command.score)

            uok.post_repository.update(post)
            uok.commit()
