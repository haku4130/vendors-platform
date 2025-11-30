from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session

from app.api.deps import CurrentVendorAccount, SessionDep
from app.crud import requests as crud
from app.models import (
    ProjectVendorRequest,
    ProjectVendorRequestPublic,
    RequestStatus,
    User,
)

router = APIRouter(prefix="/requests", tags=["requests"])


def base_process_request(
    *,
    request_id: UUID,
    session: Session,
    current_vendor: User,
) -> ProjectVendorRequest:
    req = crud.get_request_by_id(session=session, request_id=request_id)
    if not req:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Request not found")

    if not req.vendor or req.vendor.user_id != current_vendor.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    if req.status != RequestStatus.sent:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Request already processed")

    return req


@router.post("/{request_id}/accept", response_model=ProjectVendorRequestPublic)
def accept_project(
    request_id: UUID,
    session: SessionDep,
    current_vendor: CurrentVendorAccount,
):
    req = base_process_request(
        request_id=request_id,
        session=session,
        current_vendor=current_vendor,
    )

    req = crud.update_request_status(
        session=session,
        request_id=req.id,
        new_status=RequestStatus.accepted,
    )

    return req


@router.post("/{request_id}/decline", response_model=ProjectVendorRequestPublic)
def decline_project(
    request_id: UUID,
    session: SessionDep,
    current_vendor: CurrentVendorAccount,
):
    req = base_process_request(
        request_id=request_id,
        session=session,
        current_vendor=current_vendor,
    )

    req = crud.update_request_status(
        session=session,
        request_id=req.id,
        new_status=RequestStatus.declined,
    )

    return req
