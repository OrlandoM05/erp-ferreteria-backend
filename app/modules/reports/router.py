from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.core.dependencies import require_role
from app.modules.reports import service

from app.modules.products.models import Product
from app.modules.sales.models import Sale
from app.modules.inventory.models import Inventory

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/top-products")
def top_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    data = service.top_selling_products(db, limit)
    return [{"product": name, "total_sold": total} for name, total in data]


@router.get("/low-products")
def low_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    data = service.least_selling_products(db, limit)
    return [{"product": name, "total_sold": total} for name, total in data]


@router.get("/profit")
def profit(
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    return {"total_profit": service.total_profit(db)}


@router.get("/dashboard")
def dashboard_metrics(
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    return {
        "total_products": db.query(Product).count(),
        "total_sales": db.query(Sale).count(),
        "low_stock": db.query(Inventory).filter(Inventory.quantity < 5).count(),
    }


@router.get("/sales")
def sales_report(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    query = db.query(Sale)

    if start_date:
        query = query.filter(Sale.created_at >= datetime.fromisoformat(start_date))

    if end_date:
        query = query.filter(Sale.created_at <= datetime.fromisoformat(end_date))

    sales = query.all()

    total = sum(s.total for s in sales)  # 🔥 FIX

    return {
        "total": total,
        "count": len(sales),
        "sales": [
            {
                "id": s.id,
                "total": s.total,  # 🔥 FIX
                "date": s.created_at,
            }
            for s in sales
        ],
    }


@router.get("/sales-by-day")
def sales_by_day(
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    return service.sales_by_day(db)