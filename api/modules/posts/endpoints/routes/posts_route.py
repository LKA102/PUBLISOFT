from modules.posts.endpoints.dependencies import get_message_bus
from modules.posts.endpoints.dependencies import get_unit_of_work
from modules.posts.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.posts.application.message_bus import MessageBus
from modules.posts.endpoints.schemas.requests import PostCreate
from modules.posts.endpoints.schemas.requests import PostCreateForm
from modules.posts.endpoints.schemas.requests import PostUpdate
from modules.posts.endpoints.schemas.requests import PostScore
from modules.posts.endpoints.schemas.responses import CreatePostResponse
from modules.posts.endpoints.schemas.responses import PostResponse
from modules.posts.endpoints.schemas.responses import UpdatePostResponse
from modules.posts.endpoints.schemas.responses import DeletePostResponse
from modules.posts.endpoints.schemas.responses import ScorePostResponse
from modules.posts.domain.commands.post_commands import CreatePostCommand
from modules.posts.domain.commands.post_commands import UpdatePostCommand
from modules.posts.domain.commands.post_commands import DeletePostCommand
from modules.posts.domain.commands.post_commands import ScorePostCommand
from modules.posts.domain.entities.post import Post, PostTypeEnum
from modules.posts.domain.value_objects.vo import CategoryVO

from fastapi import APIRouter, Depends, status, UploadFile, Form
from fastapi.responses import JSONResponse

from common.exceptions import APIHTTPException
import traceback
from uuid import UUID


router = APIRouter()


@router.get("/all")
def get_posts(uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    posts = uok.posts_repository.load_all()

    # Convert Post entities to PostResponse objects for JSON serialization
    post_responses = []
    for post in posts:
        post_response = PostResponse(
            id=str(post.id),
            title=post.title,
            file_url=post.file_url,
            original_filename=post.original_filename,
            category=str(post.category),
            type=post.type.value,
            score_avg=post.score_avg,
            author_id=str(post.author_id),
            created_at=post.created_at.isoformat() if post.created_at else None,
            updated_at=post.updated_at.isoformat() if post.updated_at else None,
        )
        post_responses.append(post_response)

    print(post_responses)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[post_response.dict() for post_response in post_responses],
    )


@router.get("/posts/{post_id}")
def get_post(
    post_id: str, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)
):
    try:
        post = uok.posts_repository.load(UUID(post_id))
        if not post:
            raise APIHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )
    except APIHTTPException as e:
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail},
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"},
        )

    return PostResponse(
        id=str(post.id),
        title=post.title,
        file_url=post.file_url,
        original_filename=post.original_filename,
        category=str(post.category),
        type=post.type.value,
        score_avg=post.score_avg,
        author_id=str(post.author_id),
        created_at=post.created_at.isoformat() if post.created_at else None,
        updated_at=post.updated_at.isoformat() if post.updated_at else None,
    )


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_post(
    title: str = Form(...),
    category: str = Form(...),
    post_type: str = Form(...),
    author_id: str = Form(...),
    upload_file: UploadFile = None,
    uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        command = CreatePostCommand(
            title=title,
            file=upload_file,
            category=CategoryVO(name=category),
            type=PostTypeEnum(post_type),
            author_id=UUID(author_id),
        )

        results = message_bus.handle(command, uok)
        created_post: Post = results[0]

        return CreatePostResponse(
            message="Post created successfully",
            post=PostResponse(
                id=str(created_post.id),
                title=created_post.title,
                file_url=created_post.file_url,
                original_filename=created_post.original_filename,
                category=str(created_post.category),
                type=created_post.type.value,
                score_avg=created_post.score_avg,
                author_id=str(created_post.author_id),
                created_at=(
                    created_post.created_at.isoformat()
                    if created_post.created_at
                    else None
                ),
                updated_at=(
                    created_post.updated_at.isoformat()
                    if created_post.updated_at
                    else None
                ),
            ),
        )
    except APIHTTPException as e:
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail},
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"},
        )


@router.put("/update")
def update_post(
    post: PostUpdate,
    uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        command = UpdatePostCommand(
            post_id=UUID(post.post_id),
            title=post.title,
            file_url=post.file_url,
            category=CategoryVO(name=post.category),
            type=PostTypeEnum(post.type),
        )

        results = message_bus.handle(command, uok)
        updated_post: Post = results[0]

        return UpdatePostResponse(
            message="Post updated successfully",
            post=PostResponse(
                id=str(updated_post.id),
                title=updated_post.title,
                file_url=updated_post.file_url,
                original_filename=updated_post.original_filename,
                category=str(updated_post.category),
                type=updated_post.type.value,
                score_avg=updated_post.score_avg,
                author_id=str(updated_post.author_id),
                created_at=(
                    updated_post.created_at.isoformat()
                    if updated_post.created_at
                    else None
                ),
                updated_at=(
                    updated_post.updated_at.isoformat()
                    if updated_post.updated_at
                    else None
                ),
            ),
        )
    except APIHTTPException as e:
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail},
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"},
        )


@router.post("/delete")
def delete_post(
    post_id: str,
    uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        command = DeletePostCommand(post_id=UUID(post_id))
        message_bus.handle(command, uok)
        return DeletePostResponse(
            message="Post deleted successfully",
        )
    except APIHTTPException as e:
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail},
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"},
        )


@router.post("/score")
def score_post(
    score: PostScore,
    uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        command = ScorePostCommand(
            post_id=UUID(score.post_id),
            student_id=UUID(score.student_id),
            score=score.score,
        )

        message_bus.handle(command, uok)

        return ScorePostResponse(
            message="Post scored successfully",
        )
    except APIHTTPException as e:
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail},
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"},
        )
