from uuid import UUID

from sqlmodel import Session, select

from app.models import ProjectRequest, RequestInitiator, RequestStatus


def get_request(
    *, session: Session, project_id: UUID, vendor_profile_id: UUID
) -> ProjectRequest | None:
    return session.exec(
        select(ProjectRequest).where(
            ProjectRequest.project_id == project_id,
            ProjectRequest.vendor_profile_id == vendor_profile_id,
        )
    ).first()


def get_request_by_id(*, session: Session, request_id: UUID) -> ProjectRequest | None:
    return session.get(ProjectRequest, request_id)


def create_request(
    *,
    session: Session,
    project_id: UUID,
    vendor_profile_id: UUID,
    initiator: RequestInitiator,
) -> ProjectRequest:
    request = ProjectRequest(
        project_id=project_id,
        vendor_profile_id=vendor_profile_id,
        status=RequestStatus.sent,
        initiator=initiator,
    )

    session.add(request)
    session.commit()
    session.refresh(request)

    return request


def update_request_status(
    *, session: Session, request_id: UUID, new_status: RequestStatus
) -> ProjectRequest:
    request = session.get(ProjectRequest, request_id)
    if not request:
        raise
    request.status = new_status

    session.add(request)
    session.commit()
    session.refresh(request)

    return request
