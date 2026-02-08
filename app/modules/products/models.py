from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.registry import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    margin: Mapped[float | None] = mapped_column(Float)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)

    barcode: Mapped[str | None] = mapped_column(String(100), unique=True)
    margin: Mapped[float | None] = mapped_column(Float)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

    is_active: Mapped[bool] = mapped_column(default=True)
