from common.event import Event
from uuid import UUID


class ScorePostEvent(Event):
    def __init__(self, post_id: UUID, student_id: UUID, score: int):
        self.post_id = post_id
        self.student_id = student_id
        self.score = score


class PostCreatedEvent(Event):
    def __init__(self, post_id: UUID, title: str, category: str, type: str):
        self.post_id = post_id
        self.title = title
        self.category = category
        self.type = type
