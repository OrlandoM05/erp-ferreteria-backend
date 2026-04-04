from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.products.service import resolve_margin
from app.modules.suppliers.models import ProductSupplier
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


# --------------------------------------------------
# Crear categoría
# --------------------------------------------------
@router.post("/categories", response_model=CategoryResponse)
def create_category_endpoint(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    category = Category(**data.dict())
    return repository.create_category(db, category)


# --------------------------------------------------
# Crear producto
# --------------------------------------------------
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


# --------------------------------------------------
# Listar productos
# --------------------------------------------------
@router.get("", response_model=list[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    return db.query(Product).all()


# --------------------------------------------------
# Buscar por código de barras (simple)
# --------------------------------------------------
@router.get("/by-barcode/{barcode}", response_model=ProductResponse)
def get_product_by_barcode(
    barcode: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente", "Vendedor")),
):
    product = db.query(Product).filter(Product.barcode == barcode).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# --------------------------------------------------
# POS (precio dinámico)
# --------------------------------------------------
@router.get("/pos/{barcode}")
def get_product_for_pos(
    barcode: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente", "Vendedor")),
):
    product = db.query(Product).filter(Product.barcode == barcode).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    ps = (
        db.query(ProductSupplier)
        .filter(ProductSupplier.product_id == product.id)
        .order_by(ProductSupplier.created_at.desc())
        .first()
    )

    margin = resolve_margin(product) or 0

    # 🔥 CASO 1: tiene proveedor → precio real
    if ps:
        price = ps.price * (1 + margin / 100)
    else:
        # 🔥 CASO 2: fallback (NO rompe el sistema)
        price = 100 * (1 + margin / 100)

    return {
        "id": product.id,
        "name": product.name,
        "price": price,
        "barcode": product.barcode
    }