from modules.ranking.domain.commands.ranking_commands import CreateRankingCommand
from modules.ranking.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.ranking.application.message_bus import MessageBus
from common.session import SessionLocal

class RankingPublicAPI:
    def __init__(self):
        self.__uow = SqlAlchemyUnitOfWork(session_factory=SessionLocal)
        self.__message_bus = MessageBus()

    def create_ranking(self, ranking_data):
        command = CreateRankingCommand(
            student_id=ranking_data.get("student_id"),
            score=ranking_data.get("score"),
            created_at=ranking_data.get("created_at")
        )
        return self.__message_bus.handle(command, uok=self.__uow)