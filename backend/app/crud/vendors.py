from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import and_, not_
from sqlalchemy.orm import selectinload
from sqlmodel import Session, col, func, select

from app.crud import requests as requests_crud
from app.models import (
    Project,
    ProjectRequest,
    ProjectServiceLink,
    Service,
    VendorProfile,
    VendorProfileCreate,
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

    vendors = session.exec(
        select(VendorProfile).where(col(VendorProfile.id).not_in(existing_vendor_ids))
    ).all()

    if required_services_count == 0:
        return [(vendor, 0.0) for vendor in vendors][skip : skip + limit], len(vendors)

    ranked: list[tuple[VendorProfile, float]] = []
    for vendor in vendors:
        vendor_services = {s.id for s in vendor.services}
        match_count = len(required_services & vendor_services)

        score = match_count / required_services_count
        ranked.append((vendor, score))

    ranked.sort(key=lambda x: (-x[1], -len({s.id for s in x[0].services})))

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
