from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session

from app.api.deps import CurrentCompanyAccount, SessionDep
from app.crud import projects as projects_crud
from app.crud import shortlist as crud
from app.crud import vendors as vendors_crud
from app.models import Message, VendorProfilePublic

router = APIRouter(prefix="/shortlist", tags=["shortlist"])


def check_project_ownership(
    *, session: Session, project_id: UUID, current_user: CurrentCompanyAccount
) -> None:
    project = projects_crud.get_project(session=session, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this project",
        )


@router.post(
    "/projects/{project_id}/vendors/{vendor_profile_id}",
    response_model=Message,
    status_code=201,
)
def add_vendor_to_shortlist(
    session: SessionDep,
    current_user: CurrentCompanyAccount,
    project_id: UUID,
    vendor_profile_id: UUID,
) -> Message:
    """Add vendor to project shortlist (company only)"""
    check_project_ownership(
        session=session, project_id=project_id, current_user=current_user
    )

    # Verify vendor exists
    vendor = vendors_crud.get_vendor_profile(
        session=session, vendor_profile_id=vendor_profile_id
    )
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found"
        )

    crud.add_to_shortlist(
        session=session, project_id=project_id, vendor_profile_id=vendor_profile_id
    )
    return Message(message="Vendor added to shortlist")


@router.delete(
    "/projects/{project_id}/vendors/{vendor_profile_id}",
    response_model=Message,
)
def remove_vendor_from_shortlist(
    session: SessionDep,
    current_user: CurrentCompanyAccount,
    project_id: UUID,
    vendor_profile_id: UUID,
) -> Message:
    """Remove vendor from project shortlist (company only)"""
    check_project_ownership(
        session=session, project_id=project_id, current_user=current_user
    )

    removed = crud.remove_from_shortlist(
        session=session, project_id=project_id, vendor_profile_id=vendor_profile_id
    )
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not in shortlist",
        )
    return Message(message="Vendor removed from shortlist")


@router.get(
    "/projects/{project_id}/vendors",
    response_model=list[VendorProfilePublic],
)
def get_shortlisted_vendors(
    session: SessionDep,
    current_user: CurrentCompanyAccount,
    project_id: UUID,
) -> list[VendorProfilePublic]:
    """Get all vendors in project shortlist (company only)"""
    check_project_ownership(
        session=session, project_id=project_id, current_user=current_user
    )

    vendors = crud.get_shortlisted_vendors_for_project(
        session=session, project_id=project_id
    )
    return [
        vendors_crud.enrich_vendor_profile_with_reviews(
            session=session, vendor_profile=vendor
        )
        for vendor in vendors
    ]
