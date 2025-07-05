from modules.posts.domain.events.post_events import ScorePostEvent


class PostsEventHandler:
    @staticmethod
    def handle_score_post_event(event: ScorePostEvent):
        pass
        # TODO: Send notification to Notifications aggregate
        # from modules.notifications.public_api.contracts import NotificationsPublicAPI
        # notifications_api = NotificationsPublicAPI()
        # notifications_api.send_notification()
