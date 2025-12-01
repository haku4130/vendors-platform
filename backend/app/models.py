import datetime as dt
import enum
import uuid
from typing import Optional

import sqlalchemy as sa
from pydantic import EmailStr
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Enum, Field, Relationship, SQLModel

from .m2m_models import ProjectServiceLink, VendorServiceLink


class UserRole(str, enum.Enum):
    vendor = "vendor"
    company = "company"


class ProjectStart(str, enum.Enum):
    within_30_days = "Within 30 days"
    within_60_days = "Within 60 days"
    after_60_days = "After 60+ days"


class RequestStatus(str, enum.Enum):
    sent = "sent"
    accepted = "accepted"
    declined = "declined"


class RequestInitiator(str, enum.Enum):
    company = "company"
    vendor = "vendor"


class UserBaseRequired(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    company_name: str = Field(max_length=255)
    location: str = Field(max_length=255)
    role: UserRole
    full_name: str = Field(max_length=255)


class UserBaseOptional(SQLModel):
    logo_url: str | None = Field(default=None, max_length=255)


class UserBasePublic(UserBaseRequired, UserBaseOptional):
    pass


class UserBase(UserBasePublic):
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(UserBasePublic):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(UserBasePublic):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    logo_url: str | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    vendor_profile: Optional["VendorProfile"] = Relationship(
        back_populates="user"
    )  # Вынужденно используем Optional, так как использование "VendorProfile | None" невозможно
    projects: list["Project"] = Relationship(back_populates="owner")


class UserPublic(UserBasePublic):
    id: uuid.UUID
    vendor_profile: "VendorProfilePublic | None"


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class VendorProfileBase(SQLModel):
    main_goal: str
    sales_email: EmailStr
    admin_contact_phone: str
    employee_count: int
    company_website: str
    founded_year: int
    turnover: float
    description: str = Field(max_length=2000)
    min_project_size: float
    avg_hourly_rate: float


class VendorProfileCreate(VendorProfileBase):
    service_ids: list[uuid.UUID] = Field(min_length=5, max_length=10)


class VendorProfile(VendorProfileBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(
        foreign_key="user.id", unique=True, ondelete="SET NULL", nullable=True
    )
    user: User | None = Relationship(back_populates="vendor_profile")
    services: list["Service"] = Relationship(
        back_populates="vendors", link_model=VendorServiceLink
    )
    requests: list["ProjectRequest"] = Relationship(back_populates="vendor")


class VendorProfilePublic(VendorProfileBase):
    id: uuid.UUID
    user_id: uuid.UUID
    services: list["ServicePublic"]


class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


class CategoryBase(SQLModel):
    label: str = Field(max_length=255)


class Category(CategoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    services: list["Service"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SQLModel):
    label: str | None = None


class CategoryPublic(CategoryBase):
    id: uuid.UUID
    services: list["ServicePublicShort"]


class ServiceBase(SQLModel):
    label: str = Field(max_length=255)


class Service(ServiceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    category_id: uuid.UUID = Field(
        foreign_key="category.id", ondelete="SET NULL", nullable=True
    )
    category: Category = Relationship(back_populates="services")

    projects: list["Project"] = Relationship(
        back_populates="services", link_model=ProjectServiceLink
    )
    vendors: list[VendorProfile] = Relationship(
        back_populates="services", link_model=VendorServiceLink
    )


class ServiceCreate(ServiceBase):
    category_id: uuid.UUID


class ServiceUpdate(SQLModel):
    label: str | None
    category_id: uuid.UUID | None


class ServicePublicShort(ServiceBase):
    id: uuid.UUID


class ServicePublic(ServicePublicShort):
    category: Category


class ProjectBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(max_length=2000)
    start_date: ProjectStart = Field(
        sa_column=Column(
            Enum(ProjectStart, values_callable=lambda x: [e.value for e in x])
        )
    )
    location: str | None = Field(default=None, max_length=255)
    website: str | None = Field(default=None, max_length=255)
    budget: float
    questions: list[str] | None = Field(
        default=None,
        sa_column=sa.Column(JSONB),
    )
    requirements: list[str] | None = Field(
        default=None,
        sa_column=sa.Column(JSONB),
    )


class Project(ProjectBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", ondelete="SET NULL", nullable=True
    )
    owner: User | None = Relationship(back_populates="projects")
    services: list[Service] = Relationship(
        back_populates="projects", link_model=ProjectServiceLink
    )
    requests: list["ProjectRequest"] = Relationship(back_populates="project")


class ProjectCreate(ProjectBase):
    service_ids: list[uuid.UUID] = Field(min_length=5, max_length=10)


class ProjectPublic(ProjectBase):
    id: uuid.UUID
    owner: UserPublic
    services: list[Service]


class ProjectsPublic(SQLModel):
    data: list[ProjectPublic]


class ProjectRequestBase(SQLModel):
    initiator: RequestInitiator
    status: RequestStatus = Field(default=RequestStatus.sent)
    created_at: dt.datetime = Field(default_factory=lambda: dt.datetime.now(dt.UTC))
    updated_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC),
        sa_column_kwargs={
            "onupdate": lambda: dt.datetime.now(dt.UTC),
        },
    )


class ProjectRequest(ProjectRequestBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    vendor_profile_id: uuid.UUID | None = Field(
        foreign_key="vendorprofile.id", ondelete="SET NULL", nullable=True
    )
    project_id: uuid.UUID | None = Field(
        foreign_key="project.id", ondelete="SET NULL", nullable=True
    )

    project: Project | None = Relationship(back_populates="requests")
    vendor: VendorProfile | None = Relationship(back_populates="requests")


class ProjectRequestPublic(ProjectRequestBase):
    id: uuid.UUID
    vendor_profile_id: uuid.UUID
    project_id: uuid.UUID


class Message(SQLModel):
    message: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)
