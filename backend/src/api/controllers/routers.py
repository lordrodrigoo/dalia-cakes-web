from fastapi import FastAPI
from backend.src.api.controllers.admin_controller import router as admin_router


def include_routers(app: FastAPI):
    app.include_router(admin_router)
