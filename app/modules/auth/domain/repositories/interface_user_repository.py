from abc import ABC, abstractmethod
from app.modules.auth.domain.entities.user import User
from typing import Set
from uuid import UUID

class IUserRepository(ABC):
    def __init__(self):
        self.seen: Set[User] = set()

    @abstractmethod
    def _load(self, user_id: UUID) -> User:
        """
        Load a user by their ID.
        """
        pass

    @abstractmethod
    def _load_all(self) -> Set[User]:
        """
        Load all users.
        """
        pass

    @abstractmethod
    def _save(self, user: User) -> User:
        """
        Save a user to the repository.
        """
        pass

    @abstractmethod
    def _update(self, user: User) -> User:
        """
        Update an existing user in the repository.
        """
        pass

    def load(self, user_id: UUID) -> User:
        """
        Load a user by their ID, using the internal _load method.
        """
        user = self._load(user_id)
        self.seen.add(user)
        return user
    
    def load_all(self) -> Set[User]:
        """
        Load all users, using the internal _load_all method.
        """
        users = self._load_all()
        self.seen.update(users)
        return users
    
    def save(self, user: User) -> User:
        """
        Save a user to the repository, using the internal _save method.
        """
        saved_user = self._save(user)
        self.seen.add(saved_user)
        return saved_user
    
    def update(self, user: User) -> User:
        """
        Update an existing user in the repository, using the internal _update method.
        """
        updated_user = self._update(user)
        self.seen.add(updated_user)
        return updated_user