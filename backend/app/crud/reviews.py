from collections.abc import Sequence
from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import Session, col, func, select

from app.crud import vendors as vendors_crud
from app.models import Review, ReviewCreate


def create_review(*, session: Session, author_id: UUID, data: ReviewCreate) -> Review:
    # Prevent self-review
    if author_id == data.reviewed_user_id:
        raise ValueError("Cannot review yourself")

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
    result = session.exec(stmt).one()  # type: ignore
    avg_rating, count = result
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
