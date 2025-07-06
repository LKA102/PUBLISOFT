from modules.posts.endpoints.dependencies import get_message_bus
from modules.posts.endpoints.dependencies import get_unit_of_work
from modules.posts.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.posts.application.message_bus import MessageBus
from modules.posts.endpoints.schemas.requests import PostCreate
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
from modules.posts.domain.entities.post import Post

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from common.exceptions import APIHTTPException
import traceback


router = APIRouter()


@router.get("/posts")
def get_posts(uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    posts = uok.post_repository.load_all()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=posts,
    )


@router.get("/posts/{post_id}")
def get_post(
    post_id: str, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)
):
    try:
        post = uok.post_repository.load(post_id)
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

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=PostResponse(
            id=post.id,
            title=post.title,
            file_url=post.file_url,
            category=post.category,
            type=post.type,
            score_avg=post.score_avg,
            created_at=post.created_at,
            updated_at=post.updated_at,
        ),
    )


@router.post("/create")
def create_post(
    post: PostCreate,
    uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        command = CreatePostCommand(
            title=post.title,
            file=post.file,
            category=post.category,
            type=post.type,
        )

        results = message_bus.handle(command, uok)
        created_post: Post = results[0]

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=CreatePostResponse(
                message="Post created successfully",
                post=PostResponse(
                    id=created_post.id,
                    title=created_post.title,
                    file_url=created_post.file_url,
                    category=created_post.category,
                    type=created_post.type,
                    score_avg=created_post.score_avg,
                    created_at=created_post.created_at,
                    updated_at=created_post.updated_at,
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
            post_id=post.post_id,
            title=post.title,
            file_url=post.file_url,
            category=post.category,
            type=post.type,
        )

        results = message_bus.handle(command, uok)
        updated_post: Post = results[0]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=UpdatePostResponse(
                message="Post updated successfully",
                post=PostResponse(
                    id=updated_post.id,
                    title=updated_post.title,
                    file_url=updated_post.file_url,
                    category=updated_post.category,
                    type=updated_post.type,
                    score_avg=updated_post.score_avg,
                    created_at=updated_post.created_at,
                    updated_at=updated_post.updated_at,
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
        command = DeletePostCommand(post_id=post_id)
        message_bus.handle(command, uok)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=DeletePostResponse(
                message="Post deleted successfully",
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


@router.post("/score")
def score_post(
    score: PostScore,
    uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        command = ScorePostCommand(
            post_id=score.post_id,
            student_id=score.student_id,
            score=score.score,
        )

        message_bus.handle(command, uok)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=ScorePostResponse(
                message="Post scored successfully",
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
