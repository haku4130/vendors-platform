from collections.abc import Sequence
from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import Session, col, func, select

from app.models import (
    Project,
    ProjectCreate,
    ProjectRequest,
    RequestStatus,
    Service,
)


def get_project(*, session: Session, project_id: UUID) -> Project | None:
    return session.get(Project, project_id)


def get_projects_for_owner(*, session: Session, owner_id: UUID) -> Sequence[Project]:
    projects = session.exec(
        select(Project)
        .where(Project.owner_id == owner_id)
        .order_by(col(Project.created_at).desc())
    ).all()

    if not projects:
        return []

    project_ids = [p.id for p in projects]

    counts = session.exec(
        select(ProjectRequest.project_id, func.count())
        .where(col(ProjectRequest.project_id).in_(project_ids))
        .where(ProjectRequest.initiator == "vendor")
        .where(ProjectRequest.status == "sent")
        .group_by(col(ProjectRequest.project_id))
    ).all()

    incoming_map = dict(counts)

    for p in projects:
        object.__setattr__(p, "incoming_count", incoming_map.get(p.id, 0))
        # p.incoming_count = incoming_map.get(p.id, 0) # TODO: make that work

    return projects


def create_project(*, session: Session, owner_id: UUID, data: ProjectCreate) -> Project:
    project = Project.model_validate(data, update={"owner_id": owner_id})

    session.add(project)
    session.commit()
    session.refresh(project)

    if data.service_ids:
        set_services(session, project, data.service_ids)

    return project


def set_services(session: Session, project: Project, service_ids: list[UUID]):
    stmt = select(Service).where(col(Service.id).in_(service_ids))
    project.services.extend(session.exec(stmt).all())
    session.add(project)
    session.commit()


def get_accepted_projects_for_vendor(
    *,
    session: Session,
    vendor_profile_id: UUID,
    skip: int,
    limit: int,
) -> tuple[Sequence[Project], int]:
    P = Project
    R = ProjectRequest

    stmt = (
        select(P)
        .join(R, col(R.project_id) == P.id)
        .where(
            R.vendor_profile_id == vendor_profile_id,
            R.status == RequestStatus.accepted,
        )
        .order_by(col(P.created_at).desc())
        .offset(skip)
        .limit(limit)
        .options(
            selectinload(P.services),  # type: ignore
            selectinload(P.owner),  # type: ignore
        )
    )

    projects = session.exec(stmt).all()

    total_stmt = (
        select(func.count())
        .select_from(R)
        .where(
            R.vendor_profile_id == vendor_profile_id,
            R.status == RequestStatus.accepted,
        )
    )
    total = session.exec(total_stmt).one()

    return projects, total
