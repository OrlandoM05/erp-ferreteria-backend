from datetime import datetime

from sqlalchemy import String, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.registry import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)
    credit_days: Mapped[int] = mapped_column(Integer, default=0)
    delivery_days: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(default=True)


class ProductSupplier(Base):
    __tablename__ = "product_suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))

    supplier_sku: Mapped[str] = mapped_column(String(100))
    price: Mapped[float]
    credit_days: Mapped[int]
    delivery_days: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    product = relationship("Product")
    supplier = relationship("Supplier")
