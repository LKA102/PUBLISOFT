from modules.ranking.domain.commands.ranking_commands import *
from modules.ranking.domain.entities.ranking import Ranking, MonthTypeEnum
from modules.ranking.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from config.settings import settings

class RankingCommandHandler:
    
    @staticmethod
    def handle_create_ranking(command: CreateRankingCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            
            # Format created_at to match the expected format
            year = command.created_at.strftime('%Y')
            month = MonthTypeEnum(command.created_at.strftime('%b'))
            period = command.created_at.strftime('%Y%m')
            
            
            # Create the ranking entity
            ranking = Ranking.create(
                student_id=command.student_id,
                score=command.score,
                period=period,
                year=year,
                month=month,
            )

            # Persist the ranking entity
            uok.ranking_repository.save(ranking)
            uok.commit()