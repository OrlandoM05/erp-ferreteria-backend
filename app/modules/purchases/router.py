from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user, require_role
from app.modules.purchases import repository, service
from app.modules.purchases.models import PurchaseOrder, PurchaseOrderItem
from app.modules.purchases.schemas import (
    PurchaseOrderCreate,
    PurchaseReceiveItem,
)

router = APIRouter(prefix="/purchases", tags=["Purchases"])


@router.post("", response_model=dict)
def create_purchase_order(
    data: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    order = PurchaseOrder(supplier_id=data.supplier_id)
    repository.create_order(db, order)

    for item in data.items:
        po_item = PurchaseOrderItem(
            order_id=order.id,
            product_id=item.product_id,
            supplier_sku=item.supplier_sku,
            price=item.price,
            quantity_ordered=item.quantity,
        )
        repository.create_order_item(db, po_item)

    return {"order_id": order.id}


@router.post("/{order_id}/receive")
def receive_purchase(
    order_id: int,
    items: list[PurchaseReceiveItem],
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    order = db.get(PurchaseOrder, order_id)
    service.receive_items(db, order, items, user.id)
    return {"status": order.status}
