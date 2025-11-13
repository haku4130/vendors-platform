import enum
import uuid
from datetime import date
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from .m2m_models import ProjectServiceLink, VendorServiceLink


class UserRole(str, enum.Enum):
    vendor = "vendor"
    company = "company"


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    company_name: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    logo_url: str | None = Field(default=None, max_length=255)
    role: UserRole | None = None
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    logo_url: str | None = Field(default=None, max_length=255)
    company_name: str | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    vendor_profile: Optional["VendorProfile"] = Relationship(
        back_populates="user"
    )  # Вынужденно используем Optional, так как использование "VendorProfile | None" невозможно
    projects: list["Project"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class VendorProfileBase(SQLModel):
    employee_count: int | None = None
    founded_year: int | None = None
    turnover: float | None = None
    description: str | None = Field(default=None, max_length=2000)


class VendorProfile(VendorProfileBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(
        foreign_key="user.id", unique=True, ondelete="SET NULL", nullable=True
    )
    user: User | None = Relationship(back_populates="vendor_profile")
    services: list["Service"] = Relationship(
        back_populates="vendors", link_model=VendorServiceLink
    )


class VendorProfilePublic(VendorProfileBase):
    id: uuid.UUID
    user_id: uuid.UUID


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
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


class ServiceBase(SQLModel):
    label: str = Field(max_length=255)


class Service(ServiceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    category_id: uuid.UUID = Field(
        foreign_key="category.id", ondelete="SET NULL", nullable=True
    )
    category: Category | None = Relationship(back_populates="services")

    projects: list["Project"] = Relationship(
        back_populates="services", link_model=ProjectServiceLink
    )
    vendors: list[VendorProfile] = Relationship(
        back_populates="services", link_model=VendorServiceLink
    )


class ProjectBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    start_date: date | None = None
    location: str | None = Field(default=None, max_length=255)
    website: str | None = Field(default=None, max_length=255)


class Project(ProjectBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", ondelete="SET NULL", nullable=True
    )
    owner: User | None = Relationship(back_populates="projects")
    services: list[Service] = Relationship(
        back_populates="projects", link_model=ProjectServiceLink
    )


class ProjectPublic(ProjectBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    services: list[Service] | None = None


class ProjectsPublic(SQLModel):
    data: list[ProjectPublic]
    count: int
    services: list[Service] | None = None


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)
