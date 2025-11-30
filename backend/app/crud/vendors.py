from uuid import UUID

from sqlmodel import Session, col, select

from app.models import Service, VendorProfile, VendorProfileCreate


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
