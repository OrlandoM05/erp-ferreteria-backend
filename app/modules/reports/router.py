from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
    return [
        {"product": name, "total_sold": total}
        for name, total in data
    ]


@router.get("/low-products")
def low_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    data = service.least_selling_products(db, limit)
    return [
        {"product": name, "total_sold": total}
        for name, total in data
    ]


@router.get("/profit")
def profit(
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    return {
        "total_profit": service.total_profit(db)
    }


@router.get("/dashboard")
def dashboard_metrics(
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    total_products = db.query(Product).count()
    total_sales = db.query(Sale).count()
    low_stock = db.query(Inventory).filter(Inventory.quantity < 5).count()

    return {
        "total_products": total_products,
        "total_sales": total_sales,
        "low_stock": low_stock
    }