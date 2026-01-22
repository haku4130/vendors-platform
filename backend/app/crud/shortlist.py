from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, select

from app.m2m_models import ProjectShortlist
from app.models import VendorProfile


def add_to_shortlist(
    *, session: Session, project_id: UUID, vendor_profile_id: UUID
) -> ProjectShortlist:
    """Add vendor to project shortlist"""
    # Check if already exists
    existing = session.exec(
        select(ProjectShortlist).where(
            ProjectShortlist.project_id == project_id,
            ProjectShortlist.vendor_profile_id == vendor_profile_id,
        )
    ).first()

    if existing:
        return existing

    shortlist_entry = ProjectShortlist(
        project_id=project_id, vendor_profile_id=vendor_profile_id
    )
    session.add(shortlist_entry)
    session.commit()
    session.refresh(shortlist_entry)
    return shortlist_entry


def remove_from_shortlist(
    *, session: Session, project_id: UUID, vendor_profile_id: UUID
) -> bool:
    """Remove vendor from project shortlist"""
    entry = session.exec(
        select(ProjectShortlist).where(
            ProjectShortlist.project_id == project_id,
            ProjectShortlist.vendor_profile_id == vendor_profile_id,
        )
    ).first()

    if entry:
        session.delete(entry)
        session.commit()
        return True
    return False


def get_shortlisted_vendor_ids(*, session: Session, project_id: UUID) -> set[UUID]:
    """Get set of vendor_profile_ids that are in project's shortlist"""
    entries = session.exec(
        select(ProjectShortlist.vendor_profile_id).where(
            ProjectShortlist.project_id == project_id
        )
    ).all()
    return {vid for vid in entries if vid is not None}


def is_in_shortlist(
    *, session: Session, project_id: UUID, vendor_profile_id: UUID
) -> bool:
    """Check if vendor is in project shortlist"""
    entry = session.exec(
        select(ProjectShortlist).where(
            ProjectShortlist.project_id == project_id,
            ProjectShortlist.vendor_profile_id == vendor_profile_id,
        )
    ).first()
    return entry is not None


def get_shortlisted_vendors_for_project(
    *, session: Session, project_id: UUID
) -> Sequence[VendorProfile]:
    """Get all vendors in project's shortlist"""
    from sqlmodel import col

    stmt = (
        select(VendorProfile)
        .join(
            ProjectShortlist,
            col(ProjectShortlist.vendor_profile_id) == VendorProfile.id,
        )
        .where(ProjectShortlist.project_id == project_id)
    )
    return session.exec(stmt).all()
