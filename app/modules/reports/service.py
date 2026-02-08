from sqlalchemy.orm import Session
from sqlalchemy import func

from app.modules.sales.models import SaleItem
from app.modules.products.models import Product


def top_selling_products(db: Session, limit: int = 10):
    return (
        db.query(
            Product.name,
            func.sum(SaleItem.quantity).label("total_sold"),
        )
        .join(SaleItem, SaleItem.product_id == Product.id)
        .group_by(Product.name)
        .order_by(func.sum(SaleItem.quantity).desc())
        .limit(limit)
        .all()
    )


def least_selling_products(db: Session, limit: int = 10):
    return (
        db.query(
            Product.name,
            func.sum(SaleItem.quantity).label("total_sold"),
        )
        .join(SaleItem, SaleItem.product_id == Product.id)
        .group_by(Product.name)
        .order_by(func.sum(SaleItem.quantity))
        .limit(limit)
        .all()
    )


def total_profit(db: Session):
    return (
        db.query(func.sum(SaleItem.profit))
        .scalar()
    ) or 0
