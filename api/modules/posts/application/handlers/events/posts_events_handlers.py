from modules.posts.domain.events.post_events import ScorePostEvent
from modules.posts.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


class PostsEventHandler:
    @staticmethod
    def handle_score_post_event(
        event: ScorePostEvent, uok: SqlAlchemyUnitOfWork
    ):
        # TODO: remove return when Notifications aggregate is implemented
        return
        with uok:
            post = uok.posts_repository.load(event.post_id)
            if not post:
                raise ValueError("Post not found")

        notification = {
            "user_emisor_id": event.student_id,
            "user_receptor_id": post.author_id,
            "type": "APPRECIATION",
            "title": "Te han calificado",
            "message": "Se ha calificado tu publicación con una puntuación de "
            + event.score,
        }

        from modules.notifications.public_api.contracts import (
            NotificationsPublicAPI,
        )

        notifications_api = NotificationsPublicAPI()
        notifications_api.send_notification(notification)
