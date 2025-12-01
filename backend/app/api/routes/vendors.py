from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, CurrentVendorProfile, SessionDep
from app.crud import vendors as crud
from app.models import UserRole, VendorProfileCreate, VendorProfilePublic

router = APIRouter(prefix="/vendors", tags=["vendors"])


@router.get("/me", response_model=VendorProfilePublic)
def get_my_vendor_profile(current_vendor_profile: CurrentVendorProfile):
    return current_vendor_profile


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

    if current_user.vendor_profile:
        raise HTTPException(status.HTTP_409_CONFLICT, "Profile already exists")

    return crud.create_vendor_profile(
        session=session, user_id=current_user.id, data=data
    )
