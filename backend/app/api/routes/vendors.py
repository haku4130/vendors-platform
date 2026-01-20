from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, CurrentVendorProfile, SessionDep
from app.crud import projects as projects_crud
from app.crud import requests as requests_crud
from app.crud import vendors as crud
from app.models import (
    PaginatedProjectRequestsPublicProjectFull,
    PaginatedProjectsPublic,
    UserRole,
    VendorProfileCreate,
    VendorProfilePublic,
)

router = APIRouter(prefix="/vendors", tags=["vendors"])


@router.get("/me", response_model=VendorProfilePublic)
def get_my_vendor_profile(current_vendor_profile: CurrentVendorProfile):
    return current_vendor_profile


@router.get("/{vendor_profile_id}", response_model=VendorProfilePublic)
def get_vendor_profile(
    session: SessionDep, vendor_profile_id: UUID
) -> VendorProfilePublic:
    """Get vendor profile by ID (public endpoint)"""
    vendor_profile = crud.get_vendor_profile(
        session=session, vendor_profile_id=vendor_profile_id
    )
    if not vendor_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vendor profile not found"
        )
    return crud.enrich_vendor_profile_with_reviews(
        session=session, vendor_profile=vendor_profile
    )


@router.post("/me", response_model=VendorProfilePublic)
def create_vendor_profile(
    session: SessionDep,
    current_user: CurrentUser,
    data: VendorProfileCreate,
):
    if current_user.role != UserRole.vendor:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Only vendors can create vendor profiles"
        )

    if current_user.vendor_profile:
        raise HTTPException(status.HTTP_409_CONFLICT, "Profile already exists")

    return crud.create_vendor_profile(
        session=session, user_id=current_user.id, data=data
    )


@router.get(
    "/available-projects",
    response_model=PaginatedProjectsPublic,
)
def get_available_projects_for_vendor(
    session: SessionDep,
    current_vendor: CurrentVendorProfile,
    skip: int = 0,
    limit: int = 50,
):
    rows, total = crud.get_available_ranked_projects_for_vendor(
        session=session,
        vendor_profile_id=current_vendor.id,
        skip=skip,
        limit=limit,
    )

    return {"result": [project for project, _ in rows], "total": total}


@router.get(
    "/me/requests/incoming",
    response_model=PaginatedProjectRequestsPublicProjectFull,
)
def get_incoming_requests_for_vendor(
    session: SessionDep,
    current_vendor: CurrentVendorProfile,
    skip: int = 0,
    limit: int = 100,
):
    vendor_profile_id = current_vendor.id
    requests, total = requests_crud.get_incoming_requests_for_vendor(
        session=session,
        vendor_profile_id=vendor_profile_id,
        skip=skip,
        limit=limit,
    )

    return {"result": requests, "total": total}


@router.get(
    "/me/accepted-projects",
    response_model=PaginatedProjectsPublic,
)
def get_my_accepted_projects(
    session: SessionDep,
    current_vendor: CurrentVendorProfile,
    skip: int = 0,
    limit: int = 50,
):
    projects, total = projects_crud.get_accepted_projects_for_vendor(
        session=session,
        vendor_profile_id=current_vendor.id,
        skip=skip,
        limit=limit,
    )

    return {"result": projects, "total": total}
