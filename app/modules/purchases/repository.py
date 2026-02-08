from sqlalchemy.orm import Session
from app.modules.purchases.models import PurchaseOrder, PurchaseOrderItem


def create_order(db: Session, order: PurchaseOrder):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def create_order_item(db: Session, item: PurchaseOrderItem):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
