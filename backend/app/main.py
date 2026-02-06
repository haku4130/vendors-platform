import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    return route.name


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

# Disable Swagger UI and ReDoc in non-local environments (staging/production)
docs_url = "/docs" if settings.ENVIRONMENT == "local" else None
redoc_url = "/redoc" if settings.ENVIRONMENT == "local" else None

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=docs_url,
    redoc_url=redoc_url,
    generate_unique_id_function=custom_generate_unique_id,
)

app.mount(
    settings.STATIC_PATH,
    StaticFiles(directory=settings.STATIC_ROOT),
    name="static",
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

# Set up Prometheus metrics
Instrumentator().instrument(app).expose(app)
