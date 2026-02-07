from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.registry import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
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