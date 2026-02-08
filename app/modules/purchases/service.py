from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.purchases.models import PurchaseOrder, PurchaseOrderItem
from app.modules.inventory.service import add_stock


def receive_items(
    db: Session,
    order: PurchaseOrder,
    items: list,
    user_id: int,
):
    for data in items:
        item = db.get(PurchaseOrderItem, data.item_id)

        if not item or item.order_id != order.id:
            raise HTTPException(status_code=404, detail="Invalid item")

        pending = item.quantity_ordered - item.quantity_received
        if data.quantity_received > pending:
            raise HTTPException(status_code=400, detail="Over receiving")

        item.quantity_received += data.quantity_received

        add_stock(
            db=db,
            product_id=item.product_id,
            quantity=data.quantity_received,
            user_id=user_id,
            reason=f"Compra #{order.id}",
        )

    if all(i.quantity_received == i.quantity_ordered for i in order.items):
        order.status = "COMPLETO"
    else:
        order.status = "PARCIAL"

    db.commit()
