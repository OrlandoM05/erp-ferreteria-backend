from sqlalchemy.orm import Session
from sqlalchemy import func

from app.modules.sales.models import Sale, SaleItem
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
    return db.query(func.sum(SaleItem.profit)).scalar() or 0


def sales_by_day(db: Session):
    # 🔥 timezone FIX AQUÍ
    local_date = func.date(
        func.timezone('America/Mexico_City', Sale.created_at)
    )

    data = (
        db.query(
            local_date.label("date"),
            func.coalesce(func.sum(Sale.total), 0).label("total"),
        )
        .group_by(local_date)
        .order_by(local_date)
        .all()
    )

    return [
        {
            "name": str(d.date),
            "ventas": float(d.total),
        }
        for d in data
    ]