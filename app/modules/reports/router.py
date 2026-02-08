from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import require_role
from app.modules.reports import service

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
