from sqlalchemy import Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.registry import Base
from app.modules.users.roles_models import Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"))
    role = relationship("Role")

    # ✅ NUEVO (PASO A5)
    branch_id: Mapped[int | None] = mapped_column(
        ForeignKey("branches.id"),
        nullable=True,
    )

    branch = relationship("Branch")
