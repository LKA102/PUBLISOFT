from abc import ABC, abstractmethod
from modules.posts.domain.entities.post import Post
from typing import Set, List
from uuid import UUID


class IPostRepository(ABC):
    def __init__(self):
        self.seen: Set[Post] = set()

    @abstractmethod
    def _load(self, post_id: UUID) -> Post:
        """
        Load a post by its ID.
        """
        pass

    @abstractmethod
    def _load_all(self, filters: dict = None) -> List[Post]:
        """
        Load all posts.
        """
        pass

    @abstractmethod
    def _save(self, post: Post) -> Post:
        """
        Save a post to the repository.
        """
        pass

    @abstractmethod
    def _update(self, post: Post) -> Post:
        """
        Update a post in the repository.
        """
        pass

    @abstractmethod
    def _delete(self, post_id: UUID) -> None:
        """
        Delete a post from the repository.
        """
        pass

    def load(self, post_id: UUID) -> Post:
        """
        Load a post by its ID, using the internal _load method.
        """
        post = self._load(post_id)
        self.seen.add(post)
        return post

    def load_all(self, filters: dict = None) -> List[Post]:
        """
        Load all posts, using the internal _load_all method.
        """
        posts = self._load_all(filters)
        self.seen.update(posts)
        return posts

    def save(self, post: Post) -> Post:
        """
        Save a post to the repository, using the internal _save method.
        """
        saved_post = self._save(post)
        self.seen.add(saved_post)
        return saved_post

    def update(self, post: Post) -> Post:
        """
        Update a post in the repository, using the internal _update method.
        """
        updated_post = self._update(post)
        self.seen.add(updated_post)
        return updated_post

    def delete(self, post_id: UUID) -> None:
        """
        Delete a post from the repository, using the internal _delete method.
        """
        self._delete(post_id)
        # self.seen.add(post_id)
