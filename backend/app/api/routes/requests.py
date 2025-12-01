from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session

from app.api.deps import CurrentUser, SessionDep
from app.crud import requests as crud
from app.models import (
    ProjectRequest,
    ProjectRequestPublic,
    RequestInitiator,
    RequestStatus,
    User,
    UserRole,
)

router = APIRouter(prefix="/requests", tags=["requests"])


def process_request_status_change(
    *,
    request_id: UUID,
    session: Session,
    current_user: User,
) -> ProjectRequest:
    req = crud.get_request_by_id(session=session, request_id=request_id)
    if not req:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Request not found")

    if req.initiator == RequestInitiator.company:
        if (
            not current_user.role == UserRole.vendor
            or not current_user.vendor_profile
            or req.vendor_profile_id != current_user.vendor_profile.id
        ):
            raise HTTPException(status.HTTP_403_FORBIDDEN)

    if req.initiator == RequestInitiator.vendor:
        if not current_user.role == UserRole.company or (
            req.project and req.project.owner_id != current_user.id
        ):
            raise HTTPException(status.HTTP_403_FORBIDDEN)

    if req.status != RequestStatus.sent:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Request already processed")

    return req


@router.post("/{request_id}/accept", response_model=ProjectRequestPublic)
def accept_project(
    request_id: UUID,
    session: SessionDep,
    current_user: CurrentUser,
):
    req = process_request_status_change(
        request_id=request_id,
        session=session,
        current_user=current_user,
    )

    req = crud.update_request_status(
        session=session,
        request_id=req.id,
        new_status=RequestStatus.accepted,
    )

    return req


@router.post("/{request_id}/decline", response_model=ProjectRequestPublic)
def decline_project(
    request_id: UUID,
    session: SessionDep,
    current_user: CurrentUser,
):
    req = process_request_status_change(
        request_id=request_id,
        session=session,
        current_user=current_user,
    )

    req = crud.update_request_status(
        session=session,
        request_id=req.id,
        new_status=RequestStatus.declined,
    )

    return req
