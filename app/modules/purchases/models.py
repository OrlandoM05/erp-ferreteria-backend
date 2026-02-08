from datetime import datetime

from sqlalchemy import ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.registry import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    status: Mapped[str] = mapped_column(String(20), default="PEDIDO")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    items = relationship("PurchaseOrderItem", back_populates="order")


class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("purchase_orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    supplier_sku: Mapped[str]
    price: Mapped[float]

    quantity_ordered: Mapped[int]
    quantity_received: Mapped[int] = mapped_column(default=0)

    order = relationship("PurchaseOrder", back_populates="items")
