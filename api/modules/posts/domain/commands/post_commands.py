from common.command import Command
from modules.posts.domain.value_objects.vo import CategoryVO
from modules.posts.domain.entities.post import PostTypeEnum

from uuid import UUID


class CreatePostCommand(Command):
    def __init__(
        self,
        title: str,
        file_url: str,
        category: CategoryVO,
        type: PostTypeEnum,
    ):
        self.title = title
        self.file_url = file_url
        self.category = category
        self.type = type


class UpdatePostCommand(Command):
    def __init__(
        self,
        post_id: UUID,
        title: str,
        file_url: str,
        category: CategoryVO,
        type: PostTypeEnum,
    ):
        self.post_id = post_id
        self.title = title
        self.file_url = file_url
        self.category = category
        self.type = type


class DeletePostCommand(Command):
    def __init__(self, post_id: UUID):
        self.post_id = post_id


class ScorePostCommand(Command):
    def __init__(self, post_id: UUID, student_id: UUID, score: int):
        self.post_id = post_id
        self.student_id = student_id
        self.score = score
