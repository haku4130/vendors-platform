from collections.abc import Sequence
from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import Session, col, func, select

from app.crud import vendors as vendors_crud
from app.models import Project, Review, ReviewCreate, User, VendorProfile


def has_shared_project(
    *, session: Session, author_id: UUID, reviewed_user_id: UUID
) -> bool:
    """Check if two users have worked together on a project"""
    author = session.get(User, author_id)
    reviewed = session.get(User, reviewed_user_id)

    if not author or not reviewed:
        return False

    # Get vendor profile for vendor users
    author_vendor_profile = None
    reviewed_vendor_profile = None

    if author.role.value == "vendor":
        author_vendor_profile = session.exec(
            select(VendorProfile).where(col(VendorProfile.user_id) == author_id)
        ).first()

    if reviewed.role.value == "vendor":
        reviewed_vendor_profile = session.exec(
            select(VendorProfile).where(col(VendorProfile.user_id) == reviewed_user_id)
        ).first()

    # Check for shared projects
    # Case 1: author is company, reviewed is vendor
    if author.role.value == "company" and reviewed_vendor_profile:
        stmt = select(Project).where(
            col(Project.owner_id) == author_id,
            col(Project.vendor_profile_id) == reviewed_vendor_profile.id,
        )
        project = session.exec(stmt).first()
        return project is not None

    # Case 2: author is vendor, reviewed is company
    if author_vendor_profile and reviewed.role.value == "company":
        stmt = select(Project).where(
            col(Project.owner_id) == reviewed_user_id,
            col(Project.vendor_profile_id) == author_vendor_profile.id,
        )
        project = session.exec(stmt).first()
        return project is not None

    # Both are same role - no shared projects possible
    return False


def create_review(*, session: Session, author_id: UUID, data: ReviewCreate) -> Review:
    # Prevent self-review
    if author_id == data.reviewed_user_id:
        raise ValueError("Cannot review yourself")

    # Check if users have worked together
    if not has_shared_project(
        session=session, author_id=author_id, reviewed_user_id=data.reviewed_user_id
    ):
        raise ValueError("You can only review users you have worked with on a project")

    review = Review.model_validate(data, update={"author_id": author_id})
    session.add(review)
    session.commit()
    session.refresh(review)
    return review


def get_reviews_for_user(
    *,
    session: Session,
    user_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> tuple[Sequence[Review], int]:
    total_stmt = select(func.count(col(Review.id))).where(
        col(Review.reviewed_user_id) == user_id
    )
    total = session.exec(total_stmt).one()

    stmt = (
        select(Review)
        .where(col(Review.reviewed_user_id) == user_id)
        .options(selectinload(Review.author), selectinload(Review.reviewed_user))  # type: ignore
        .order_by(col(Review.created_at).desc())
        .offset(skip)
        .limit(limit)
    )

    return session.exec(stmt).all(), total


def get_reviews_for_vendor(
    *,
    session: Session,
    vendor_profile_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> tuple[Sequence[Review], int]:
    """Get reviews for a vendor by vendor_profile_id"""

    vendor_profile = vendors_crud.get_vendor_profile(
        session=session, vendor_profile_id=vendor_profile_id
    )
    if not vendor_profile or not vendor_profile.user_id:
        return [], 0

    return get_reviews_for_user(
        session=session,
        user_id=vendor_profile.user_id,
        skip=skip,
        limit=limit,
    )


def get_reviews_by_author(
    *,
    session: Session,
    author_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> tuple[Sequence[Review], int]:
    total_stmt = (
        select(func.count())
        .select_from(Review)
        .where(col(Review.author_id) == author_id)
    )
    total = session.exec(total_stmt).one()

    stmt = (
        select(Review)
        .where(col(Review.author_id) == author_id)
        .options(selectinload(Review.author), selectinload(Review.reviewed_user))  # type: ignore
        .order_by(col(Review.created_at).desc())
        .offset(skip)
        .limit(limit)
    )

    return session.exec(stmt).all(), total


def get_user_rating_stats(
    *, session: Session, user_id: UUID
) -> tuple[float | None, int]:
    """Returns (average_rating, reviews_count) for a user (vendor or company)"""

    stmt = select(func.avg(col(Review.rating)), func.count(col(Review.id))).where(
        col(Review.reviewed_user_id) == user_id
    )
    avg_rating, count = session.exec(stmt).one()
    return float(avg_rating) if avg_rating else None, count or 0


def get_vendor_rating_stats(
    *, session: Session, vendor_profile_id: UUID
) -> tuple[float | None, int]:
    """Returns (average_rating, reviews_count) for a vendor by vendor_profile_id"""

    vendor_profile = vendors_crud.get_vendor_profile(
        session=session, vendor_profile_id=vendor_profile_id
    )
    if not vendor_profile or not vendor_profile.user_id:
        return None, 0

    return get_user_rating_stats(session=session, user_id=vendor_profile.user_id)


def get_users_to_review(*, session: Session, current_user_id: UUID) -> Sequence[User]:
    """
    Get users that the current user can leave a review for.
    These are users from completed projects where no review has been left yet.
    """
    current_user = session.get(User, current_user_id)
    if not current_user:
        return []

    # Get IDs of users already reviewed by current user
    reviewed_user_ids_stmt = select(col(Review.reviewed_user_id)).where(
        col(Review.author_id) == current_user_id
    )
    reviewed_user_ids = set(session.exec(reviewed_user_ids_stmt).all())

    if current_user.role.value == "company":
        # For companies: get vendors from their projects where an executor was selected
        stmt = (
            select(User)
            .join(VendorProfile, col(VendorProfile.user_id) == col(User.id))
            .join(Project, col(Project.vendor_profile_id) == col(VendorProfile.id))
            .where(
                col(Project.owner_id) == current_user_id,
                col(Project.vendor_profile_id).is_not(None),
                col(User.id).not_in(reviewed_user_ids) if reviewed_user_ids else True,
            )
            .distinct()
        )
    else:
        # For vendors: get companies from projects where they were selected as executor
        vendor_profile = session.exec(
            select(VendorProfile).where(col(VendorProfile.user_id) == current_user_id)
        ).first()

        if not vendor_profile:
            return []

        stmt = (
            select(User)
            .join(Project, col(Project.owner_id) == col(User.id))
            .where(
                col(Project.vendor_profile_id) == vendor_profile.id,
                col(User.id).not_in(reviewed_user_ids) if reviewed_user_ids else True,
            )
            .distinct()
        )

    return session.exec(stmt).all()
