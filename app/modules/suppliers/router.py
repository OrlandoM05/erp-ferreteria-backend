from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import require_role
from app.modules.suppliers import repository
from app.modules.suppliers.models import Supplier, ProductSupplier
from app.modules.suppliers.schemas import (
    SupplierCreate,
    SupplierResponse,
    ProductSupplierCreate,
)

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.post("", response_model=SupplierResponse)
def create_supplier_endpoint(
    data: SupplierCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    supplier = Supplier(**data.dict())
    return repository.create_supplier(db, supplier)


@router.post("/product", response_model=dict)
def link_product_supplier(
    data: ProductSupplierCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    ps = ProductSupplier(**data.dict())
    repository.create_product_supplier(db, ps)
    return {"status": "linked"}
