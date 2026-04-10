#pylint: disable=unused-import
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from backend.src.exceptions.handlers import register_exception_handlers
from backend.src.middlewares.middlewares import setup_middlewares
from backend.src.config.settings import Settings
from backend.src.config.logger import setup_logging
from backend.src.config.owner import ensure_owner
from backend.src.api.controllers.routers import include_routers

load_dotenv()
setup_logging()


_env = os.getenv("ENV", "development")

@asynccontextmanager
async def lifespan(_app: FastAPI):
    ensure_owner()
    yield


app = FastAPI(
    title=Settings.API_TITLE,
    version=Settings.API_VERSION,
    docs_url="/docs" if _env != "production" else None,
    redoc_url="/redoc" if _env != "production" else None,
    openapi_url="/openapi.json" if _env != "production" else None,
    lifespan=lifespan,
)


# MIDDLEWARE
setup_middlewares(app)

# EXCEPTION HANDLERS
register_exception_handlers(app)

# ROUTES
include_routers(app)
