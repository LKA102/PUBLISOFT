from modules.posts.domain.entities.post import Post, PostTypeEnum
from modules.posts.domain.value_objects.vo import CategoryVO
from modules.posts.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.posts.domain.commands.post_commands import CreatePostCommand
from modules.posts.domain.commands.post_commands import UpdatePostCommand
from modules.posts.domain.commands.post_commands import DeletePostCommand
from modules.posts.domain.commands.post_commands import ScorePostCommand
from config.settings import supabase_client, settings


class PostsCommandHandler:
    @staticmethod
    def handle_create_post_command(
        command: CreatePostCommand, uok: SqlAlchemyUnitOfWork
    ) -> Post:
        with uok:
            category = command.category
            post_type = command.type

            # Read the file content as bytes
            file_content = command.file.file.read()
            # Reset file pointer to beginning for potential future reads
            command.file.file.seek(0)

            # Debug file information
            print(f"File name: {command.file.filename}")
            print(f"File content type: {command.file.content_type}")
            print(f"File size: {len(file_content)} bytes")

            # Generate unique filename to avoid conflicts
            import time
            import hashlib

            # Create a unique filename with timestamp and hash
            timestamp = int(time.time())
            file_hash = hashlib.md5(
                f"{command.file.filename}{timestamp}".encode()
            ).hexdigest()[:8]
            file_extension = (
                command.file.filename.split(".")[-1]
                if "." in command.file.filename
                else ""
            )
            unique_filename = (
                f"{timestamp}_{file_hash}.{file_extension}"
                if file_extension
                else f"{timestamp}_{file_hash}"
            )

            print(f"Unique filename: {unique_filename}")

            try:
                # Try with bytes directly first
                upload_response = supabase_client.storage.from_(
                    "publisoft-posts"
                ).upload(
                    path=f"public/{unique_filename}",
                    file=file_content,
                    file_options={
                        "content-type": command.file.content_type
                        or "application/octet-stream"
                    },
                )
                print(f"Upload response: {upload_response}")

                # Get the public URL for the uploaded file
                file_url = supabase_client.storage.from_(
                    "publisoft-posts"
                ).get_public_url(f"public/{unique_filename}")
                print(f"File URL: {file_url}")

            except Exception as e:
                print(f"Upload error: {e}")
                print(f"Error type: {type(e)}")
                print(f"Error details: {str(e)}")
                print(f"Full error: {repr(e)}")

                # Try alternative approach with storage3 directly
                try:
                    from storage3 import create_client as create_storage_client

                    storage_client = create_storage_client(
                        settings.SUPABASE_URL, settings.SUPABASE_KEY
                    )

                    upload_response = storage_client.from_(
                        "publisoft-posts"
                    ).upload(
                        path=f"public/{unique_filename}",
                        file=file_content,
                        file_options={
                            "content-type": command.file.content_type
                            or "application/octet-stream"
                        },
                    )
                    print(f"Alternative upload response: {upload_response}")

                    file_url = storage_client.from_(
                        "publisoft-posts"
                    ).get_public_url(f"public/{unique_filename}")
                    print(f"Alternative file URL: {file_url}")

                except Exception as e2:
                    print(f"Alternative upload also failed: {e2}")
                    raise e  # Re-raise the original error

            post = Post.create(
                title=command.title,
                file_url=file_url,
                original_filename=command.file.filename,
                category=category,
                post_type=post_type,
            )

            saved_post = uok.posts_repository.save(post)
            uok.commit()

            return saved_post

    @staticmethod
    def handle_update_post_command(
        command: UpdatePostCommand, uok: SqlAlchemyUnitOfWork
    ) -> Post:
        with uok:
            post = uok.posts_repository.load(command.post_id)
            if not post:
                raise ValueError("Post not found")

            if command.category:
                category = command.category
            if command.type:
                post_type = command.type

            if command.title:
                post.title = command.title
            if command.file_url:
                post.file_url = command.file_url
            if command.category:
                post.category = category
            if command.type:
                post.type = post_type

            updated_post = uok.posts_repository.update(post)
            uok.commit()

            return updated_post

    @staticmethod
    def handle_delete_post_command(
        command: DeletePostCommand, uok: SqlAlchemyUnitOfWork
    ):
        with uok:
            post = uok.posts_repository.load(command.post_id)
            if not post:
                raise ValueError("Post not found")

            uok.posts_repository.delete(command.post_id)
            uok.commit()

    @staticmethod
    def handle_score_post_command(
        command: ScorePostCommand, uok: SqlAlchemyUnitOfWork
    ):
        with uok:
            post = uok.posts_repository.load(command.post_id)
            if not post:
                raise ValueError("Post not found")

            post.score_post(command.student_id, command.score)

            uok.posts_repository.update(post)
            uok.commit()
