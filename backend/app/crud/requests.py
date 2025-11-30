from uuid import UUID

from sqlmodel import Session, select

from app.models import ProjectVendorRequest, RequestStatus


def get_request(
    *, session: Session, project_id: UUID, vendor_profile_id: UUID
) -> ProjectVendorRequest | None:
    return session.exec(
        select(ProjectVendorRequest).where(
            ProjectVendorRequest.project_id == project_id,
            ProjectVendorRequest.vendor_profile_id == vendor_profile_id,
        )
    ).first()


def get_request_by_id(
    *, session: Session, request_id: UUID
) -> ProjectVendorRequest | None:
    return session.get(ProjectVendorRequest, request_id)


def create_request(
    *, session: Session, project_id: UUID, vendor_profile_id: UUID
) -> ProjectVendorRequest:
    request = ProjectVendorRequest(
        project_id=project_id,
        vendor_profile_id=vendor_profile_id,
        status=RequestStatus.sent,
    )

    session.add(request)
    session.commit()
    session.refresh(request)

    return request


def update_request_status(
    *, session: Session, request_id: UUID, new_status: RequestStatus
) -> ProjectVendorRequest:
    request = session.get(ProjectVendorRequest, request_id)
    if not request:
        raise
    request.status = new_status

    session.add(request)
    session.commit()
    session.refresh(request)

    return request
