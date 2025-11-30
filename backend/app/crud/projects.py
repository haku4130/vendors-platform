from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, col, select

from app.models import Project, ProjectCreate, Service


def get_project(*, session: Session, project_id: UUID) -> Project | None:
    return session.get(Project, project_id)


def get_projects_for_owner(*, session: Session, owner_id: UUID) -> Sequence[Project]:
    stmt = select(Project).where(Project.owner_id == owner_id)
    return session.exec(stmt).all()


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
