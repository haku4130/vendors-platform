import uuid

from sqlmodel import Field, SQLModel


class ProjectServiceLink(SQLModel, table=True):
    project_id: uuid.UUID | None = Field(
        default=None, foreign_key="project.id", primary_key=True
    )
    service_id: uuid.UUID | None = Field(
        default=None, foreign_key="service.id", primary_key=True
    )


class VendorServiceLink(SQLModel, table=True):
    vendor_profile_id: uuid.UUID | None = Field(
        default=None, foreign_key="vendorprofile.id", primary_key=True
    )
    service_id: uuid.UUID | None = Field(
        default=None, foreign_key="service.id", primary_key=True
    )


class ProjectShortlist(SQLModel, table=True):
    project_id: uuid.UUID | None = Field(
        default=None, foreign_key="project.id", primary_key=True, ondelete="CASCADE"
    )
    vendor_profile_id: uuid.UUID | None = Field(
        default=None,
        foreign_key="vendorprofile.id",
        primary_key=True,
        ondelete="CASCADE",
    )
