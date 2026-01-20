from fastapi import APIRouter

from app.api.routes import (
    items,
    login,
    private,
    projects,
    requests,
    reviews,
    services,
    users,
    utils,
    vendors,
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(vendors.router)
api_router.include_router(services.router)
api_router.include_router(projects.router)
api_router.include_router(requests.router)
api_router.include_router(reviews.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
