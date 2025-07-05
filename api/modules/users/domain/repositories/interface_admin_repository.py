from abc import ABC, abstractmethod
from modules.users.domain.entities.admin import Admin
from typing import Set
from uuid import UUID

class IAdminRepository(ABC):
    def __init__(self):
        self.seen: Set[Admin] = set()

    @abstractmethod
    def _load(self, admin_id: UUID) -> Admin:
        """
        Load an admin by their ID.
        """
        pass

    @abstractmethod
    def _load_all(self) -> Set[Admin]:
        """
        Load all admins.
        """
        pass

    @abstractmethod
    def _save(self, admin: Admin) -> Admin:
        """
        Save an admin to the repository.
        """
        pass

    @abstractmethod
    def _update(self, admin: Admin) -> Admin:
        """
        Update an existing admin in the repository.
        """
        pass

    def load(self, admin_id: UUID) -> Admin:
        """
        Load an admin by their ID, using the internal _load method.
        """
        admin = self._load(admin_id)
        self.seen.add(admin)
        return admin
    
    def load_all(self) -> Set[Admin]:
        """
        Load all admins, using the internal _load_all method.
        """
        admins = self._load_all()
        self.seen.update(admins)
        return admins
    
    def save(self, admin: Admin) -> Admin:
        """
        Save an admin to the repository, using the internal _save method.
        """
        saved_admin = self._save(admin)
        self.seen.add(saved_admin)
        return saved_admin
    
    def update(self, admin: Admin) -> Admin:
        """
        Update an existing admin in the repository, using the internal _update method.
        """
        updated_admin = self._update(admin)
        self.seen.add(updated_admin)
        return updated_admin