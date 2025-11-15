from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app import projects_crud as crud
from app.api.deps import CurrentCompanyAccount, SessionDep
from app.models import ProjectCreate, ProjectPublic

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
