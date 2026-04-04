from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.registry import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)

    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(Integer, default=0)
    min_quantity: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        UniqueConstraint("branch_id", "product_id"),
    )

    product = relationship("Product")


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    branch_id: Mapped[int] = mapped_column(  # ✅ agregado (importante)
        ForeignKey("branches.id"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    type: Mapped[str] = mapped_column(String(20))  # IN / OUT
    quantity: Mapped[int]
    reason: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    product = relationship("Product")