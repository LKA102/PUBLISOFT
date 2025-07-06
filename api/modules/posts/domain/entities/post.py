from modules.posts.domain.entities.base_entity import BaseEntity
from modules.posts.domain.value_objects.vo import CategoryVO, ScoreVO

# from modules.posts.domain.events.post_events import ScorePostEvent
from modules.posts.domain.events.post_events import PostCreatedEvent

from typing import List
import enum
from uuid import UUID
from datetime import datetime, timezone


class PostTypeEnum(str, enum.Enum):
    NOTE = "NOTE"
    SYLLABUS = "SYLLABUS"
    STUDY_PLAN = "STUDY_PLAN"
    ACADEMIC_INFO = "ACADEMIC_INFO"


class Post(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__title = kwargs.get("title")
        self.__file_url = kwargs.get("file_url")
        self.__original_filename = kwargs.get("original_filename")
        self.__category: CategoryVO = kwargs.get("category")
        self.__type: PostTypeEnum = kwargs.get("type")
        self.__scores: List[ScoreVO] = kwargs.get("scores")
        self.__score_avg: float = kwargs.get("score_avg")

        self.events = set()

    def __eq__(self, other):
        if not isinstance(other, Post):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def title(self) -> str:
        return self.__title

    @property
    def file_url(self) -> str:
        return self.__file_url

    @property
    def original_filename(self) -> str:
        return self.__original_filename

    @property
    def category(self) -> CategoryVO:
        return self.__category

    @property
    def type(self) -> PostTypeEnum:
        return self.__type

    @property
    def scores(self) -> List[ScoreVO]:
        return self.__scores

    @property
    def score_avg(self) -> float:
        return self.__score_avg

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Title must be a non-empty string")
        self.__title = value

    @file_url.setter
    def file_url(self, value: str):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("File URL must be a non-empty string")
        self.__file_url = value

    @original_filename.setter
    def original_filename(self, value: str):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Original filename must be a non-empty string")
        self.__original_filename = value

    @category.setter
    def category(self, value: CategoryVO):
        if not isinstance(value, CategoryVO):
            raise ValueError("Category must be an instance of CategoryVO")
        self.__category = value

    @type.setter
    def type(self, value: PostTypeEnum):
        if not isinstance(value, PostTypeEnum):
            raise ValueError("Type must be an instance of PostTypeEnum")
        self.__type = value

    @scores.setter
    def scores(self, value: List[ScoreVO]):
        if not isinstance(value, List):
            raise ValueError("Scores must be a list")
        self.__scores = value

    @score_avg.setter
    def score_avg(self, value: float):
        if not isinstance(value, float):
            raise ValueError("Score average must be a float")
        self.__score_avg = value

    @classmethod
    def create(
        cls,
        title: str,
        file_url: str,
        original_filename: str,
        category: CategoryVO,
        post_type: PostTypeEnum,
    ) -> "Post":

        if not title or len(title) == 0:
            raise ValueError("Title must be a non-empty string")

        post_id = UUID(int=0)  # Placeholder ID
        created_at = updated_at = datetime.now(timezone.utc)

        post = cls(
            id=post_id,
            title=title,
            file_url=file_url,
            original_filename=original_filename,
            category=category,
            type=post_type,
            scores=[],
            score_avg=0.0,
            created_at=created_at,
            updated_at=updated_at,
        )

        post_created_event = PostCreatedEvent(
            post_id=post.id if post.id else None,
            title=post.title,
            category=str(post.category),
            type=post.type.value,
        )
        post.events.add(post_created_event)

        return post

    def score_post(self, student_id: UUID, score: int) -> None:
        """
        Scores the current post.
        A student can score a post only once.
        """
        if not ScoreVO.is_valid_score(score):
            raise ValueError("Score must be an integer between 1 and 5")

        for existing_score in self.__scores:
            if existing_score.student_id == student_id:
                raise ValueError("Student has already scored this post")

        self.__scores.append(ScoreVO(student_id=student_id, score=score))
        self.__score_avg = sum(score.score for score in self.__scores) / len(
            self.__scores
        )

        # TODO: uncomment when Notifications aggregate is implemented
        # post_score_event = ScorePostEvent(
        #     post_id=self.id, student_id=student_id, score=score
        # )
        # self.events.add(post_score_event)
