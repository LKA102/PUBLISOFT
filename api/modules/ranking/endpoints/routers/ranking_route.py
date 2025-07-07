from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.responses import JSONResponse
#from modules.ranking.application.views.ranking_view import RankingView
from modules.ranking.endpoints.dependencies import get_message_bus, get_unit_of_work
from modules.ranking.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.ranking.application.message_bus import MessageBus
from common.exceptions import APIHTTPException
from modules.ranking.endpoints.schemas.requests import RankingCreate
from modules.ranking.domain.commands.ranking_commands import CreateRankingCommand
import traceback

router = APIRouter()


@router.get("/list")
def list_ranking():
    pass

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_ranking(ranking: RankingCreate, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    try:
    
        command = CreateRankingCommand(
            student_id=ranking.student_id,
            score=ranking.score,
            created_at=ranking.created_at
        )
        
        message_bus.handle(command, uok=uok)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Ranking created successfully"}
        )
    
    except APIHTTPException as e:
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"}
        )
    
    