from abc import ABC, abstractmethod
from modules.notifications.domain.entities.notification import Notification
from typing import Set
from uuid import UUID

class INotificationRepository(ABC):
    def __init__(self):
        self.seen: Set[Notification] = set()

    @abstractmethod
    def _load(self, notification_id: int) -> Notification:
        """
        Load a notification by its ID.
        """
        pass

    @abstractmethod
    def _load_all(self) -> Set[Notification]:
        """
        Load all notifications.
        """
        pass

    @abstractmethod
    def _save(self, notification: Notification) -> Notification:
        """
        Save a notification to the repository.
        """
        pass

    @abstractmethod
    def _update(self, notification: Notification) -> Notification:
        """
        Update an existing notification in the repository.
        """
        pass

    def load(self, notification_id: int) -> Notification:
        """
        Load a notification by its ID, using the internal _load method.
        """
        notification = self._load(notification_id)
        self.seen.add(notification)
        return notification

    def load_all(self) -> Set[Notification]:
        """
        Load all notifications, using the internal _load_all method.
        """
        notifications = self._load_all()
        self.seen.update(notifications)
        return notifications

    def save(self, notification: Notification) -> Notification:
        """
        Save a notification to the repository, using the internal _save method.
        """
        saved_notification = self._save(notification)
        self.seen.add(saved_notification)
        return saved_notification

    def update(self, notification: Notification) -> Notification:
        """
        Update an existing notification in the repository, using the internal _update method.
        """
        updated_notification = self._update(notification)
        self.seen.add(updated_notification)
        return updated_notification