from abc import ABC, abstractmethod
from domain.entities.user_entity import UserEntity

class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(self, user: UserEntity) -> None:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> UserEntity:
        pass