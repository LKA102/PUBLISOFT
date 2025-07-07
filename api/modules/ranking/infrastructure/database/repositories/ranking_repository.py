from typing import Set, Optional
from modules.ranking.domain.entities.ranking import Ranking
from modules.ranking.domain.repositories.interface_ranking_repository import IRankingRepository
from modules.ranking.infrastructure.database.models.ranking import RankingSQLAlchemy
from modules.ranking.infrastructure.database.mapper.ranking_mapper import RankingMapper
from uuid import UUID

class RankingRepositorySQLAlchemy(IRankingRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _save(self, ranking: Ranking) -> Ranking:
        ranking_orm = RankingMapper.to_orm(ranking)
        self.session.add(ranking_orm)
        return ranking

    def _load(self, ranking_id: int) -> Optional[Ranking]:
        ranking_orm = self.session.query(RankingSQLAlchemy).filter_by(id=ranking_id).first()
        if not ranking_orm:
            return None
        return RankingMapper.to_entity(ranking_orm)

    def _load_all(self) -> Set[Ranking]:
        rankings_orm = self.session.query(RankingSQLAlchemy).all()
        return {RankingMapper.to_entity(ranking_orm) for ranking_orm in rankings_orm}

    def _update(self, ranking: Ranking) -> Optional[Ranking]:
        # Update directly in the database using session.query().update()
        update_data = {
            "period": ranking.period,
            "score": ranking.score,
            "student_id": ranking.student_id,
            "year": ranking.year,
            "month": ranking.month
        }

        # Perform the update
        rows_updated = self.session.query(RankingSQLAlchemy).filter_by(id=ranking.id).update(update_data)

        # If at least one row was updated, return the updated entity
        if rows_updated:
            updated_ranking_orm = self.session.query(RankingSQLAlchemy).filter_by(id=ranking.id).first()
            return RankingMapper.to_entity(updated_ranking_orm)
        else:
            return None