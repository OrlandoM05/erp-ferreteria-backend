from datetime import datetime

from sqlalchemy import ForeignKey, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.registry import Base


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # 🔥 FIX (AGREGADO)
    branch_id: Mapped[int] = mapped_column(Integer)

    total: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    items = relationship("SaleItem", back_populates="sale")


class SaleItem(Base):
    __tablename__ = "sale_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    quantity: Mapped[int]
    price: Mapped[float]
    cost: Mapped[float]
    profit: Mapped[float]

    sale = relationship("Sale", back_populates="items")