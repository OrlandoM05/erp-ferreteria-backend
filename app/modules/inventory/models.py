from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.registry import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), unique=True)

    quantity: Mapped[int] = mapped_column(Integer, default=0)
    min_quantity: Mapped[int] = mapped_column(Integer, default=0)

    product = relationship("Product")


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    type: Mapped[str] = mapped_column(String(20))  # IN / OUT
    quantity: Mapped[int]
    reason: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    product = relationship("Product")
