from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, col, func, select

from app.models import PlatformFeedback, PlatformFeedbackCreate


def create_feedback(
    *, session: Session, user_id: UUID, data: PlatformFeedbackCreate
) -> PlatformFeedback:
    fb = PlatformFeedback.model_validate(data, update={"user_id": user_id})
    session.add(fb)
    session.commit()
    session.refresh(fb)
    return fb


def list_feedback(
    *, session: Session, skip: int = 0, limit: int = 100
) -> tuple[Sequence[PlatformFeedback], int]:
    total = session.exec(select(func.count()).select_from(PlatformFeedback)).one()

    stmt = (
        select(PlatformFeedback)
        .order_by(col(PlatformFeedback.created_at).desc())
        .offset(skip)
        .limit(limit)
    )
    return session.exec(stmt).all(), total
