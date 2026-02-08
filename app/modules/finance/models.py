from datetime import datetime, date

from sqlalchemy import ForeignKey, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.registry import Base


class Payable(Base):
    __tablename__ = "payables"

    id: Mapped[int] = mapped_column(primary_key=True)

    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    purchase_order_id: Mapped[int] = mapped_column(ForeignKey("purchase_orders.id"))

    amount: Mapped[float]
    due_date: Mapped[date]

    status: Mapped[str] = mapped_column(String(20), default="PENDIENTE")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    supplier = relationship("Supplier")
