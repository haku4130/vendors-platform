from uuid import UUID

from sqlmodel import Session, select

from app.api.exceptions import AlreadyExistsError
from app.models import Category, Service, ServiceUpdate


# CATEGORY CRUD
def create_category(*, session: Session, label: str) -> Category:
    exists = session.exec(select(Category).where(Category.label == label)).first()
    if exists:
        raise AlreadyExistsError("Category already exists")
    category = Category(label=label)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def update_category(*, session: Session, category: Category, label: str | None):
    if label:
        category.label = label
        session.add(category)
        session.commit()
        session.refresh(category)
    return category


def get_category(*, session: Session, category_id: UUID) -> Category | None:
    return session.get(Category, category_id)


def get_categories_with_services(*, session: Session):
    stmt = select(Category)
    return session.exec(stmt).all()


# SERVICE CRUD
def create_service(*, session: Session, label: str, category_id: UUID):
    exists = session.exec(select(Service).where(Service.label == label)).first()
    if exists:
        raise AlreadyExistsError("Service already exists")
    service = Service(label=label, category_id=category_id)
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


def update_service(*, session: Session, service: Service, data: ServiceUpdate):
    service_data = data.model_dump(exclude_unset=True)
    service.sqlmodel_update(service_data)
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


def get_service(*, session: Session, service_id: UUID) -> Service | None:
    return session.get(Service, service_id)


def delete_service(*, session: Session, service: Service):
    session.delete(service)
    session.commit()
