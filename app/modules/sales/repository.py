from sqlalchemy.orm import Session
from app.modules.sales.models import Sale, SaleItem


def create_sale(db: Session, sale: Sale):
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale


def create_sale_item(db: Session, item: SaleItem):
    db.add(item)
    db.commit()
    return item
