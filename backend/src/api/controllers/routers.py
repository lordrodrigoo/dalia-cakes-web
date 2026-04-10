from fastapi import FastAPI
from backend.src.api.controllers.admin_controller import router as admin_router
from backend.src.api.controllers.category_controller import router as category_router

def include_routers(app: FastAPI):
    app.include_router(admin_router)
    app.include_router(category_router)
