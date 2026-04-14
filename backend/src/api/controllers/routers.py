from fastapi import FastAPI
from backend.src.api.controllers.admin_controller import router as admin_router
from backend.src.api.controllers.category_controller import router as category_router
from backend.src.api.controllers.product_controller import router as product_router
from backend.src.api.controllers.instagram_controller import router as instagram_router
from backend.src.api.controllers.decorated_cakes_controller import router as decorated_cakes_router
from backend.src.api.controllers.chatbot_controller import router as chatbot_router
from backend.src.api.controllers.upload_controller import router as upload_router

def include_routers(app: FastAPI):
    app.include_router(admin_router)
    app.include_router(category_router)
    app.include_router(product_router)
    app.include_router(instagram_router)
    app.include_router(decorated_cakes_router)
    app.include_router(chatbot_router)
    app.include_router(upload_router)
