import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from backend.src.config.limiter import limiter
from backend.src.middlewares.correlation_middleware import CorrelationIdMiddleware
from backend.src.middlewares.logging_middleware import LoggingMiddleware



_RAW_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in _RAW_HOSTS.split(",") if h.strip()]


# MIDDLEWARES
def setup_middlewares(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(LoggingMiddleware)
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=5)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:3000",
        ],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
