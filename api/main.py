from fastapi import FastAPI
from modules.auth import auth_controller
from modules.notifications import notifications_controller
from modules.users import users_controller
from modules.posts import posts_contoller
from modules.ranking import ranking_controller


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_controller.router)
# app.include_router(notifications_controller.router)
# app.include_router(users_controller.router)
# app.include_router(posts_controller.router)
# app.include_router(ranking_controller.router)
