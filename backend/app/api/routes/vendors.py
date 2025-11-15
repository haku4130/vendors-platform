from fastapi import APIRouter, HTTPException, status

from app import vendors_crud as crud
from app.api.deps import CurrentUser, SessionDep
from app.models import UserRole, VendorProfileCreate, VendorProfilePublic

router = APIRouter(prefix="/vendors", tags=["vendors"])


@router.get("/me", response_model=VendorProfilePublic)
def get_my_vendor_profile(session: SessionDep, current_user: CurrentUser):
    if current_user.role != UserRole.vendor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors have vendor profiles",
        )

    profile = crud.get_vendor_profile_by_id(session=session, user_id=current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vendor profile not found"
        )

    return profile


@router.post("/me", response_model=VendorProfilePublic)
def create_vendor_profile(
    session: SessionDep,
    current_user: CurrentUser,
    data: VendorProfileCreate,
):
    if current_user.role != UserRole.vendor:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Only vendors can create vendor profiles"
        )

    profile = crud.get_vendor_profile_by_id(session=session, user_id=current_user.id)
    if profile:
        raise HTTPException(status.HTTP_409_CONFLICT, "Profile already exists")

    return crud.create_vendor_profile(
        session=session, user_id=current_user.id, data=data
    )
