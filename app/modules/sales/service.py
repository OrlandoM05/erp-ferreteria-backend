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
    try:
        # 🔥 Crear venta
        sale = Sale(
            user_id=user_id,
            total=0,
            branch_id=1  # 🔥 FIX
        )

        db.add(sale)
        db.commit()
        db.refresh(sale)

        total = 0

        # 🔥 Procesar productos
        for data in items:
            product = (
                db.query(Product)
                .filter(Product.barcode == data.barcode)
                .first()
            )

            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            ps = (
                db.query(ProductSupplier)
                .filter(ProductSupplier.product_id == product.id)
                .order_by(ProductSupplier.created_at.desc())
                .first()
            )

            margin = resolve_margin(product) or 0

            # 🔥 Precio / costo
            if ps:
                price = ps.price * (1 + margin / 100)
                cost = ps.price
            else:
                price = 100 * (1 + margin / 100)
                cost = 100

            # 🔥 Descontar inventario
            remove_stock(
                db=db,
                product_id=product.id,
                quantity=data.quantity,
                user_id=user_id,
                branch_id=1,  # 👈 FIX
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

        # 🔥 Actualizar total
        sale.total = total

        db.commit()
        db.refresh(sale)

        return sale

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))