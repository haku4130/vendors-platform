from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.crud import feedback as feedback_crud
from app.models import (
    Message,
    PaginatedPlatformFeedbackPublic,
    PlatformFeedbackCreate,
    PlatformFeedbackPublic,
)

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/", status_code=201)
def submit_platform_feedback(
    session: SessionDep, current_user: CurrentUser, data: PlatformFeedbackCreate
) -> Message:
    """
    Submit feedback about the platform (authorized users only).
    """
    feedback_crud.create_feedback(session=session, user_id=current_user.id, data=data)
    return Message(message="Feedback received")


@router.get(
    "/",
    response_model=PaginatedPlatformFeedbackPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def get_feedback(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
):
    feedback, total = feedback_crud.list_feedback(
        session=session, skip=skip, limit=limit
    )
    result = [PlatformFeedbackPublic.model_validate(fb) for fb in feedback]
    return PaginatedPlatformFeedbackPublic(result=result, total=total)
