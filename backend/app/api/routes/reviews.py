from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, SessionDep
from app.crud import reviews as crud
from app.models import (
    PaginatedReviewsPublic,
    ReviewCreate,
    ReviewPublic,
)

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewPublic)
def create_review(
    session: SessionDep,
    current_user: CurrentUser,
    data: ReviewCreate,
):
    try:
        review = crud.create_review(
            session=session,
            author_id=current_user.id,
            data=data,
        )
        # Load relationships
        session.refresh(review, ["author", "reviewed_user"])  # type: ignore
        return review
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/user/{user_id}",
    response_model=PaginatedReviewsPublic,
)
def get_reviews_for_user(
    user_id: UUID,
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
):
    """Get reviews for a user (vendor or company)"""
    reviews, total = crud.get_reviews_for_user(
        session=session,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )
    return {"result": reviews, "total": total}


@router.get(
    "/vendor/{vendor_profile_id}",
    response_model=PaginatedReviewsPublic,
)
def get_reviews_for_vendor(
    vendor_profile_id: UUID,
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
):
    """Get reviews for a vendor by vendor_profile_id"""
    reviews, total = crud.get_reviews_for_vendor(
        session=session,
        vendor_profile_id=vendor_profile_id,
        skip=skip,
        limit=limit,
    )
    return {"result": reviews, "total": total}


@router.get(
    "/me",
    response_model=PaginatedReviewsPublic,
)
def get_my_reviews(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
):
    """Get reviews written by the current user"""
    reviews, total = crud.get_reviews_by_author(
        session=session,
        author_id=current_user.id,
        skip=skip,
        limit=limit,
    )
    return {"result": reviews, "total": total}


@router.get(
    "/me/received",
    response_model=PaginatedReviewsPublic,
)
def get_reviews_received_by_me(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
):
    """Get reviews received by the current user"""
    reviews, total = crud.get_reviews_for_user(
        session=session,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )
    return {"result": reviews, "total": total}
