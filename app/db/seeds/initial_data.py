from sqlalchemy.orm import Session

from app.modules.users.models import User
from app.modules.users.roles_models import Role, Permission
from app.core.security import hash_password


def seed_roles(db: Session):
    roles = ["Admin", "Gerente", "Vendedor", "Almacen"]

    existing = {r.name for r in db.query(Role).all()}

    for role_name in roles:
        if role_name not in existing:
            db.add(Role(name=role_name))

    db.commit()


def seed_permissions(db: Session):
    permissions = [
        # Products
        "products:view",
        "products:create",
        "products:update",
        "products:delete",
        # Inventory
        "inventory:view",
        "inventory:update",
        # Sales
        "sales:create",
        "sales:view",
        # Purchases
        "purchases:create",
        "purchases:view",
        # Reports
        "reports:view",
        "reports:financial",
    ]

    existing = {p.code for p in db.query(Permission).all()}

    for code in permissions:
        if code not in existing:
            db.add(Permission(code=code))

    db.commit()


def seed_admin(db: Session):
    admin_email = "admin@erp.com"

    admin_role = db.query(Role).filter(Role.name == "Admin").first()
    if not admin_role:
        return

    admin = db.query(User).filter(User.email == admin_email).first()

    if not admin:
        admin = User(
            email=admin_email,
            hashed_password=hash_password("admin123"),
            is_active=True,
            is_superuser=True,
            role=admin_role,
        )
        db.add(admin)
        db.commit()
        return

    # 🔧 corrección automática
    if not admin.role:
        admin.role = admin_role
        db.commit()



def run_seeds(db: Session):
    seed_roles(db)
    seed_permissions(db)
    seed_admin(db)
