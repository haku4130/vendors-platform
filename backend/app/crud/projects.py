from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, col, func, select

from app.models import Project, ProjectCreate, ProjectRequest, Service


def get_project(*, session: Session, project_id: UUID) -> Project | None:
    return session.get(Project, project_id)


def get_projects_for_owner(*, session: Session, owner_id: UUID) -> Sequence[Project]:
    projects = session.exec(select(Project).where(Project.owner_id == owner_id)).all()

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
