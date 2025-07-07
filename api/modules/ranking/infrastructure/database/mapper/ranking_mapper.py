from modules.ranking.domain.entities.ranking import Ranking, MonthTypeEnum
from modules.ranking.infrastructure.database.models.ranking import RankingSQLAlchemy
from modules.ranking.infrastructure.database.models.base_entity import BaseEntitySQLAlchemy


class RankingMapper:
    @staticmethod
    def to_entity(ranking_orm: RankingSQLAlchemy) -> Ranking:
        # Convert the ORM model to the domain entity
        base_kwargs = BaseEntitySQLAlchemy.orm_to_base_entity(ranking_orm)
        return Ranking(
            period=ranking_orm.period,
            score=ranking_orm.score,
            student_id=ranking_orm.student_id,
            year=ranking_orm.year,
            month=MonthTypeEnum(ranking_orm.month) if ranking_orm.month else None,
            **base_kwargs
        )

    @staticmethod
    def to_orm(ranking: Ranking) -> RankingSQLAlchemy:
        # Convert the domain entity to the ORM model
        ranking_orm = RankingSQLAlchemy()
        ranking_orm.period = ranking.period
        ranking_orm.score = ranking.score
        ranking_orm.student_id = ranking.student_id
        ranking_orm.year = ranking.year
        ranking_orm.month = ranking.month
        BaseEntitySQLAlchemy.base_entity_to_orm(ranking, ranking_orm)
        return ranking_orm