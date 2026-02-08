from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import require_role
from app.modules.products import repository, service
from app.modules.products.models import Product, Category
from app.modules.products.schemas import (
    CategoryCreate,
    CategoryResponse,
    ProductCreate,
    ProductResponse,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/categories", response_model=CategoryResponse)
def create_category_endpoint(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    category = Category(**data.dict())
    return repository.create_category(db, category)


@router.post("", response_model=ProductResponse)
def create_product_endpoint(
    data: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    sku = service.generate_sku()

    product = Product(
        sku=sku,
        name=data.name,
        barcode=data.barcode,
        margin=data.margin,
        category_id=data.category_id,
    )

    return repository.create_product(db, product)
