from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, col, func, select

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


def get_requests_for_project(
    *,
    session: Session,
    project_id: UUID,
    initiator: RequestInitiator | None = None,
    status: RequestStatus | None = None,
    skip: int = 0,
    limit: int = 100,
) -> tuple[Sequence[ProjectRequest], int]:
    filters = [ProjectRequest.project_id == project_id]

    if initiator is not None:
        filters.append(ProjectRequest.initiator == initiator)
    if status is not None:
        filters.append(ProjectRequest.status == status)

    total = session.exec(
        select(func.count()).select_from(ProjectRequest).where(*filters)
    ).one()

    stmt = (
        select(ProjectRequest)
        .where(*filters)
        .order_by(col(ProjectRequest.created_at).desc())
        .offset(skip)
        .limit(limit)
    )

    return session.exec(stmt).all(), total


def get_vendor_ids_from_project_requests(
    *, session: Session, project_id: UUID
) -> Sequence[UUID] | Sequence[None]:
    stmt = select(ProjectRequest.vendor_profile_id).where(
        ProjectRequest.project_id == project_id
    )

    return session.exec(stmt).all()


def get_incoming_requests_for_vendor(
    *, session: Session, vendor_profile_id: UUID, skip: int, limit: int
) -> tuple[Sequence[ProjectRequest], int]:
    total = session.exec(
        select(func.count())
        .select_from(ProjectRequest)
        .where(
            ProjectRequest.vendor_profile_id == vendor_profile_id,
            ProjectRequest.initiator == RequestInitiator.company,
        )
    ).one()

    stmt = (
        select(ProjectRequest)
        .where(
            ProjectRequest.vendor_profile_id == vendor_profile_id,
            ProjectRequest.initiator == RequestInitiator.company,
        )
        .order_by(col(ProjectRequest.created_at).desc())
        .offset(skip)
        .limit(limit)
    )

    return session.exec(stmt).all(), total
