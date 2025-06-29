from fastapi import APIRouter
from modules.users.endpoints.routers.admin_router import router as admin_router
from modules.users.endpoints.routers.student_router import router as student_router

router = APIRouter()

router.include_router(admin_router, prefix="/admin", tags=["admin"])
router.include_router(student_router, prefix="/student", tags=["student"])