from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, require_role
from app.modules.users.models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def read_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role.name if user.role else None,
    }


@router.get("/admin-only")
def admin_only(
    user: User = Depends(require_role("Admin")),
):
    return {"message": "Welcome admin"}
