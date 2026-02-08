from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.products.models import Product
from app.modules.inventory.service import remove_stock
from app.modules.sales.models import Sale, SaleItem
from app.modules.products.service import resolve_margin
from app.modules.suppliers.models import ProductSupplier


def process_sale(
    db: Session,
    items: list,
    user_id: int,
):
    sale = Sale(user_id=user_id, total=0)
    db.add(sale)
    db.commit()
    db.refresh(sale)

    total = 0

    for data in items:
        product = (
            db.query(Product)
            .filter(Product.barcode == data.barcode)
            .first()
        )

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # costo: último precio proveedor
        ps = (
            db.query(ProductSupplier)
            .filter(ProductSupplier.product_id == product.id)
            .order_by(ProductSupplier.created_at.desc())
            .first()
        )

        if not ps:
            raise HTTPException(status_code=400, detail="No supplier price")

        margin = resolve_margin(product) or 0
        price = ps.price * (1 + margin / 100)
        cost = ps.price

        remove_stock(
            db=db,
            product_id=product.id,
            quantity=data.quantity,
            user_id=user_id,
            reason=f"Venta #{sale.id}",
        )

        profit = (price - cost) * data.quantity
        total += price * data.quantity

        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=data.quantity,
            price=price,
            cost=cost,
            profit=profit,
        )

        db.add(sale_item)

    sale.total = total
    db.commit()
    return sale
