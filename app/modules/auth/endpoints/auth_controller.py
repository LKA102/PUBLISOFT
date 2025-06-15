from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter()

#@router.post("login")
#def login(logindata: UserLogin, response: Response, uok: UnitOfWorkSqlAlchemy = Depends(get_unit_of_work)