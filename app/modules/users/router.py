from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_role
from app.modules.users.models import User
from app.modules.users.roles_models import Role, Permission
from app.db.session import get_db

from app.modules.users.schemas import UserCreate
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def read_me(user: User = Depends(get_current_user)):
    permissions = []

    if user.role and user.role.permissions:
        permissions = [p.code for p in user.role.permissions]

    return {
        "id": user.id,
        "email": user.email,
        "role": user.role.name if user.role else None,
        "permissions": permissions,
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


# 🔥 GET ROLES
@router.get("/roles")
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()


# 🔥 GET PERMISSIONS
@router.get("/permissions")
def get_permissions(db: Session = Depends(get_db)):
    return db.query(Permission).all()


# 🔥 ASSIGN PERMISSIONS
@router.post("/roles/{role_id}/permissions")
def assign_permissions(
    role_id: int,
    permission_ids: list[int],
    db: Session = Depends(get_db),
):
    role = db.get(Role, role_id)

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # limpiar permisos actuales
    role.permissions.clear()

    # asignar nuevos
    permissions = db.query(Permission).filter(
        Permission.id.in_(permission_ids)
    ).all()

    role.permissions.extend(permissions)

    db.commit()

    return {"message": "Permissions updated"}