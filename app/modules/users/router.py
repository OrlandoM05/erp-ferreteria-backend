from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # ✅ FALTABA

from app.core.dependencies import get_current_user, require_role
from app.modules.users.models import User
from app.db.session import get_db

from app.modules.users.schemas import UserCreate  # ✅ ORDENADO ARRIBA
from app.core.security import hash_password

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


# 🔥 CREATE USER (ADMIN)
@router.post("", response_model=dict)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("Admin")),
):
    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        is_active=True,
        role_id=data.role_id,
        branch_id=data.branch_id,
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}