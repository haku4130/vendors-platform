from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentCompanyAccount, CurrentVendorProfile, SessionDep
from app.crud import projects as crud
from app.crud import requests as requests_crud
from app.crud import vendors as vendors_crud
from app.models import (
    ProjectCreate,
    ProjectPublic,
    ProjectRequestPublic,
    RequestInitiator,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectPublic])
def list_my_projects(session: SessionDep, company_account: CurrentCompanyAccount):
    return crud.get_projects_for_owner(session=session, owner_id=company_account.id)


@router.post("/", response_model=ProjectPublic)
def create_new_project(
    session: SessionDep, company_account: CurrentCompanyAccount, data: ProjectCreate
):
    return crud.create_project(session=session, owner_id=company_account.id, data=data)


@router.get("/{project_id}", response_model=ProjectPublic)
def get_project_detail(
    project_id: UUID, session: SessionDep, company_account: CurrentCompanyAccount
):
    project = crud.get_project(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    if project.owner_id != company_account.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return project


@router.post(
    "/{project_id}/request/company/{vendor_profile_id}",
    response_model=ProjectRequestPublic,
)
def send_project_request_company(
    project_id: UUID,
    vendor_profile_id: UUID,
    session: SessionDep,
    company_account: CurrentCompanyAccount,
):
    project = crud.get_project(session=session, project_id=project_id)
    if not project or project.owner_id != company_account.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found or not owned")

    vendor_profile = vendors_crud.get_vendor_profile(
        session=session, vendor_profile_id=vendor_profile_id
    )
    if not vendor_profile:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Vendor profile not found")

    existing = requests_crud.get_request(
        session=session, project_id=project_id, vendor_profile_id=vendor_profile_id
    )

    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Request already sent")

    req = requests_crud.create_request(
        session=session,
        project_id=project_id,
        vendor_profile_id=vendor_profile.id,
        initiator=RequestInitiator.company,
    )
    return req


@router.post(
    "/{project_id}/request/vendor",
    response_model=ProjectRequestPublic,
)
def send_project_request_vendor(
    project_id: UUID,
    session: SessionDep,
    current_vendor_profile: CurrentVendorProfile,
):
    project = crud.get_project(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    existing = requests_crud.get_request(
        session=session,
        project_id=project_id,
        vendor_profile_id=current_vendor_profile.id,
    )

    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Request already sent")

    req = requests_crud.create_request(
        session=session,
        project_id=project_id,
        vendor_profile_id=current_vendor_profile.id,
        initiator=RequestInitiator.vendor,
    )
    return req
