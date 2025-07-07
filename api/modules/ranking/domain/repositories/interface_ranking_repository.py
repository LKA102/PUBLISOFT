from abc import ABC, abstractmethod
from modules.ranking.domain.entities.ranking import Ranking
from typing import Set
from uuid import UUID

class IRankingRepository(ABC):
    def __init__(self):
        self.seen: Set[Ranking] = set()

    @abstractmethod
    def _load(self, ranking_id: int) -> Ranking:
        """
        Load a ranking by its ID.
        """
        pass

    @abstractmethod
    def _load_all(self) -> Set[Ranking]:
        """
        Load all rankings.
        """
        pass

    @abstractmethod
    def _save(self, ranking: Ranking) -> Ranking:
        """
        Save a ranking to the repository.
        """
        pass

    @abstractmethod
    def _update(self, ranking: Ranking) -> Ranking:
        """
        Update an existing ranking in the repository.
        """
        pass

    def load(self, ranking_id: int) -> Ranking:
        """
        Load a ranking by its ID, using the internal _load method.
        """
        ranking = self._load(ranking_id)
        self.seen.add(ranking)
        return ranking

    def load_all(self) -> Set[Ranking]:
        """
        Load all rankings, using the internal _load_all method.
        """
        rankings = self._load_all()
        self.seen.update(rankings)
        return rankings

    def save(self, ranking: Ranking) -> Ranking:
        """
        Save a ranking to the repository, using the internal _save method.
        """
        saved_ranking = self._save(ranking)
        self.seen.add(saved_ranking)
        return saved_ranking

    def update(self, ranking: Ranking) -> Ranking:
        """
        Update an existing ranking in the repository, using the internal _update method.
        """
        updated_ranking = self._update(ranking)
        self.seen.add(updated_ranking)
        return updated_ranking