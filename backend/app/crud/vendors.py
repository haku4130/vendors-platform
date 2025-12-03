from uuid import UUID

from sqlmodel import Session, col, select

from app.crud import requests as requests_crud
from app.models import Project, Service, VendorProfile, VendorProfileCreate


def get_vendor_profile(
    *, session: Session, vendor_profile_id: UUID
) -> VendorProfile | None:
    return session.get(VendorProfile, vendor_profile_id)


def get_vendor_profile_by_user_id(
    *, session: Session, user_id: UUID
) -> VendorProfile | None:
    return session.exec(
        select(VendorProfile).where(VendorProfile.user_id == user_id)
    ).first()


def create_vendor_profile(
    *, session: Session, user_id: UUID, data: VendorProfileCreate
) -> VendorProfile:
    profile = VendorProfile.model_validate(data, update={"user_id": user_id})

    session.add(profile)
    session.commit()
    session.refresh(profile)

    if data.service_ids:
        set_services(session=session, profile=profile, service_ids=data.service_ids)
    return profile


def set_services(*, session: Session, profile: VendorProfile, service_ids: list[UUID]):
    stmt = select(Service).where(col(Service.id).in_(service_ids))
    profile.services.extend(session.exec(stmt).all())
    session.add(profile)
    session.commit()


def get_ranked_vendors_for_project(
    session: Session, project: Project, skip: int, limit: int
) -> list[tuple[VendorProfile, float]]:
    required_services = {s.id for s in project.services}
    required_count = len(required_services)

    vendors = session.exec(select(VendorProfile)).all()

    existing_vendor_ids = requests_crud.get_vendor_ids_from_project_requests(
        session=session, project_id=project.id
    )
    existing_vendor_ids = {vid for vid in existing_vendor_ids if vid is not None}  # type: ignore

    vendors = session.exec(
        select(VendorProfile).where(col(VendorProfile.id).not_in(existing_vendor_ids))
    ).all()

    if required_count == 0:
        return [(vendor, 0.0) for vendor in vendors][skip : skip + limit]

    ranked: list[tuple[VendorProfile, float]] = []
    for vendor in vendors:
        vendor_services = {s.id for s in vendor.services}
        match_count = len(required_services & vendor_services)

        score = match_count / required_count
        ranked.append((vendor, score))

    ranked.sort(key=lambda x: (-x[1], -len({s.id for s in x[0].services})))

    return ranked[skip : skip + limit]
