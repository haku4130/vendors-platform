from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app import services_crud as crud
from app.api.deps import RequireSuperUser, SessionDep
from app.api.exceptions import AlreadyExistsError
from app.models import (
    CategoryCreate,
    CategoryPublic,
    CategoryUpdate,
    Message,
    ServiceCreate,
    ServicePublic,
    ServiceUpdate,
)

router = APIRouter(prefix="/catalog", tags=["catalog"])


# ---------- PUBLIC ----------
@router.get("/categories", response_model=list[CategoryPublic])
def list_categories(session: SessionDep):
    return crud.get_categories_with_services(session=session)


# ---------- ADMIN ----------
@router.post(
    "/categories",
    response_model=CategoryPublic,
    dependencies=[RequireSuperUser],
)
def create_category(data: CategoryCreate, session: SessionDep):
    try:
        return crud.create_category(session=session, label=data.label)
    except AlreadyExistsError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Category already exists")


@router.patch(
    "/categories/{category_id}",
    response_model=CategoryPublic,
    dependencies=[RequireSuperUser],
)
def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    session: SessionDep,
):
    category = crud.get_category(session=session, category_id=category_id)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found")

    return crud.update_category(session=session, category=category, label=data.label)


@router.post(
    "/services",
    response_model=ServicePublic,
    dependencies=[RequireSuperUser],
)
def create_service(
    data: ServiceCreate,
    session: SessionDep,
):
    try:
        return crud.create_service(
            session=session, label=data.label, category_id=data.category_id
        )
    except AlreadyExistsError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Service already exists")


@router.patch(
    "/services/{service_id}",
    response_model=ServicePublic,
    dependencies=[RequireSuperUser],
)
def update_service(
    service_id: UUID,
    data: ServiceUpdate,
    session: SessionDep,
):
    service = crud.get_service(session=session, service_id=service_id)
    if not service:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")

    return crud.update_service(session=session, service=service, data=data)


@router.delete(
    "/services/{service_id}",
    dependencies=[RequireSuperUser],
)
def delete_service(
    service_id: UUID,
    session: SessionDep,
) -> Message:
    service = crud.get_service(session=session, service_id=service_id)
    if not service:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")

    crud.delete_service(session=session, service=service)
    return Message(message="Service deleted successfully")
