from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import and_, not_
from sqlalchemy.orm import selectinload
from sqlmodel import Session, col, func, select

from app.crud import requests as requests_crud
from app.crud import reviews as reviews_crud
from app.crud import shortlist as shortlist_crud
from app.models import (
    Project,
    ProjectRequest,
    ProjectServiceLink,
    Service,
    VendorProfile,
    VendorProfileCreate,
    VendorProfilePublic,
    VendorServiceLink,
)


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
) -> tuple[list[tuple[VendorProfile, float]], int]:
    required_services = {s.id for s in project.services}
    required_services_count = len(required_services)

    existing_vendor_ids = requests_crud.get_vendor_ids_from_project_requests(
        session=session, project_id=project.id
    )
    existing_vendor_ids = {vid for vid in existing_vendor_ids if vid is not None}  # type: ignore

    # Get shortlisted vendor IDs for this project
    shortlisted_vendor_ids = shortlist_crud.get_shortlisted_vendor_ids(
        session=session, project_id=project.id
    )

    vendors = session.exec(
        select(VendorProfile).where(col(VendorProfile.id).not_in(existing_vendor_ids))
    ).all()

    ranked: list[tuple[VendorProfile, float]] = []

    if required_services_count == 0:
        # Even with no services, shortlisted vendors go first
        ranked = [(vendor, 0.0) for vendor in vendors]
        ranked.sort(key=lambda x: (x[0].id not in shortlisted_vendor_ids,))
        return ranked[skip : skip + limit], len(vendors)

    for vendor in vendors:
        vendor_services = {s.id for s in vendor.services}
        match_count = len(required_services & vendor_services)

        score = match_count / required_services_count
        ranked.append((vendor, score))

    # Sort: shortlisted first, then by score, then by number of services
    ranked.sort(
        key=lambda x: (
            x[0].id not in shortlisted_vendor_ids,  # False (shortlisted) first
            -x[1],  # Higher score first
            -len({s.id for s in x[0].services}),  # More services first
        )
    )

    return ranked[skip : skip + limit], len(ranked)


def get_available_ranked_projects_for_vendor(
    *,
    session: Session,
    vendor_profile_id: UUID,
    skip: int,
    limit: int,
) -> tuple[Sequence[tuple[Project, int]], int]:
    # Алиасы для удобства
    P = Project
    PSL = ProjectServiceLink
    R = ProjectRequest
    VSL = VendorServiceLink

    # Подзапрос: существуют ли заявки между этим проектом и этим вендором?
    subq_exists = (
        select(R.id)
        .where(
            R.project_id == P.id,
            R.vendor_profile_id == vendor_profile_id,
        )
        .exists()
    )

    total = session.exec(
        select(func.count()).select_from(P).where(not_(subq_exists))
    ).one()

    # Счётчик пересечений сервисов
    similarity_count = func.count(col(VSL.service_id)).label("similarity_score")

    stmt = (
        select(P, similarity_count)
        .join(PSL, col(PSL.project_id) == P.id, isouter=True)
        .join(
            VSL,
            and_(
                col(VSL.service_id) == PSL.service_id,
                col(VSL.vendor_profile_id) == vendor_profile_id,
            ),
            isouter=True,
        )
        .where(
            not_(subq_exists),  # нет существующих заявок с этой компанией
        )
        .group_by(col(P.id))
        .order_by(
            similarity_count.desc(),
            col(P.created_at).desc(),
        )
        .offset(skip)
        .limit(limit)
        .options(
            selectinload(P.services),  # type: ignore
            selectinload(P.owner),  # type: ignore
        )
    )

    rows = session.exec(stmt).all()

    return rows, total


def search_vendors(
    *,
    session: Session,
    service_ids: list[UUID] | None = None,
    location: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> tuple[list[VendorProfile], int]:
    """
    Search for vendors by services and optionally by location.
    Returns vendors sorted by relevance (number of matching services).
    """
    from app.models import User

    # If service IDs are provided, filter vendors with matching services
    if service_ids and len(service_ids) > 0:
        # Get all vendors that have at least one of the requested services
        vendors_query = (
            select(VendorProfile)
            .join(
                VendorServiceLink,
                col(VendorServiceLink.vendor_profile_id) == col(VendorProfile.id),
            )
            .where(col(VendorServiceLink.service_id).in_(service_ids))
            .distinct()
        )

        # Apply location filter if provided
        if location:
            vendors_query = vendors_query.join(
                User, col(VendorProfile.user_id) == col(User.id)
            ).where(func.lower(col(User.location)).contains(location.lower()))

        # Get all matching vendors for sorting
        all_vendors = session.exec(vendors_query).all()

        # Sort by number of matching services
        required_services = set(service_ids)
        vendors_with_score = []

        for vendor in all_vendors:
            # Load services relationship
            session.refresh(vendor, ["services"])
            vendor_services = {s.id for s in vendor.services}
            match_count = len(required_services & vendor_services)
            vendors_with_score.append((vendor, match_count))

        # Sort by match count descending
        vendors_with_score.sort(key=lambda x: -x[1])

        # Get total and apply pagination
        total = len(vendors_with_score)
        paginated_vendors = [v for v, _ in vendors_with_score[skip : skip + limit]]

        return paginated_vendors, total

    # No service filter - just get all vendors (optionally filtered by location)
    query = select(VendorProfile)

    if location:
        query = query.join(User, col(VendorProfile.user_id) == col(User.id)).where(
            func.lower(col(User.location)).contains(location.lower())
        )

    # Get total count
    count_query = select(func.count()).select_from(VendorProfile)
    if location:
        count_query = count_query.join(
            User, col(VendorProfile.user_id) == col(User.id)
        ).where(func.lower(col(User.location)).contains(location.lower()))

    total = session.exec(count_query).one()

    # Apply pagination
    vendors = session.exec(query.offset(skip).limit(limit)).all()

    return list(vendors), total


def enrich_vendor_profile_with_reviews(
    *, session: Session, vendor_profile: VendorProfile
) -> VendorProfilePublic:
    """Enrich VendorProfile with rating and reviews count"""
    # Ensure relationships are loaded
    session.refresh(vendor_profile, ["user", "services"])  # type: ignore

    if not vendor_profile.user_id:
        vendor_public = VendorProfilePublic.model_validate(vendor_profile)
        vendor_public.rating = None
        vendor_public.reviewsCount = 0
        return vendor_public

    rating, reviews_count = reviews_crud.get_user_rating_stats(
        session=session, user_id=vendor_profile.user_id
    )

    # Convert to VendorProfilePublic
    vendor_public = VendorProfilePublic.model_validate(vendor_profile)
    vendor_public.rating = rating
    vendor_public.reviewsCount = reviews_count

    return vendor_public
